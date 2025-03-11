from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json
import spacy
from models import db, User, StudyPlan, Progress
from config import Config
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle
import os
from rl_model import StudySchedulerRL

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database and login manager
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Load spaCy model for NLP with a fallback
try:
    nlp = spacy.load('en_core_web_sm')
except Exception as e:
    print(f"Warning: Could not load spaCy model 'en_core_web_sm'. Falling back to simple parsing. Error: {e}")
    nlp = None

# Google Calendar API setup
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
        else:
            # Use 'pbkdf2:sha256' instead of 'sha256'
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/sync_calendar/<int:plan_id>')
@login_required
def sync_calendar(plan_id):
    plan = StudyPlan.query.get_or_404(plan_id)
    schedule = json.loads(plan.schedule)

    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    for day in schedule:
        date = datetime.strptime(day['date'], '%Y-%m-%d')
        for item in day['schedule']:
            start_time = datetime.strptime(f"{day['date']} {item['time']}", '%Y-%m-%d %H:%M')
            end_time = start_time + timedelta(hours=item['duration'])
            event = {
                'summary': f"Study: {item['subject']}",
                'start': {'dateTime': start_time.isoformat(), 'timeZone': 'UTC'},
                'end': {'dateTime': end_time.isoformat(), 'timeZone': 'UTC'},
            }
            service.events().insert(calendarId='primary', body=event).execute()

    flash('Study plan synced with Google Calendar!')
    return redirect(url_for('index'))

def parse_subjects_with_nlp(subject_string):
    if nlp:
        doc = nlp(subject_string)
        subjects = []
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT', 'NOUN']:
                subjects.append(ent.text)
        if not subjects:
            subjects = [token.text for token in doc if token.pos_ == 'NOUN']
        return subjects if subjects else subject_string.split(',')
    else:
        # Fallback to simple comma-separated parsing
        return [s.strip() for s in subject_string.split(',')]

def generate_study_plan_with_rl(subjects, deadline, hours_per_day):
    today = datetime.now()
    days_available = (deadline - today).days + 1
    if days_available < 1:
        return None

    scheduler = StudySchedulerRL(len(subjects), days_available)
    plan = []
    current_date = today

    for day in range(days_available):
        daily_schedule = []
        remaining_hours = hours_per_day

        while remaining_hours > 0:
            state = day
            subject_idx = scheduler.choose_action(state)
            subject = subjects[subject_idx]
            duration = min(2, remaining_hours)
            start_time = (9 + (hours_per_day - remaining_hours)) % 24

            daily_schedule.append({
                'time': f"{int(start_time):02d}:00",
                'subject': subject,
                'duration': duration
            })

            reward = 1.0
            scheduler.update(state, subject_idx, reward, (day + 1) % days_available)

            remaining_hours -= duration

        plan.append({
            'date': (current_date + timedelta(days=day)).strftime('%Y-%m-%d'),
            'schedule': daily_schedule
        })

    return plan

@app.route('/progress/<int:plan_id>', methods=['GET', 'POST'])
@login_required
def progress(plan_id):
    plan = StudyPlan.query.get_or_404(plan_id)
    schedule = json.loads(plan.schedule)
    if request.method == 'POST':
        task_id = request.form['task_id']
        completed = request.form.get('completed') == 'on'
        progress_entry = Progress.query.get(task_id)
        if progress_entry:
            progress_entry.completed = completed
            db.session.commit()
        return redirect(url_for('progress', plan_id=plan_id))
    
    progress_data = Progress.query.filter_by(study_plan_id=plan_id).all()
    return render_template('progress.html', plan=plan, schedule=schedule, progress_data=progress_data)

@app.route('/generate-plan', methods=['POST'])
@login_required
def generate_plan():
    data = request.get_json()
    try:
        subjects = parse_subjects_with_nlp(data['subjects'])
        deadline = datetime.strptime(data['deadline'], '%Y-%m-%d')
        hours_per_day = int(data['hours_per_day'])

        plan = generate_study_plan_with_rl(subjects, deadline, hours_per_day)
        if not plan:
            return jsonify({'success': False, 'message': 'Deadline must be in the future'})

        new_plan = StudyPlan(
            user_id=current_user.id,
            subjects=','.join(subjects),
            deadline=deadline,
            hours_per_day=hours_per_day,
            schedule=json.dumps(plan)
        )
        db.session.add(new_plan)
        db.session.commit()

        for day in plan:
            for item in day['schedule']:
                progress_entry = Progress(
                    study_plan_id=new_plan.id,
                    date=day['date'],
                    task=f"{item['time']}: {item['subject']} ({item['duration']} hours)",
                    completed=False
                )
                db.session.add(progress_entry)
        db.session.commit()

        return jsonify({'success': True, 'plan': plan, 'plan_id': new_plan.id})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/')
@login_required
def index():
    plans = StudyPlan.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', plans=plans)

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
    
