# AI Study Planner

A web application designed to help students create and manage personalized study plans using reinforcement learning (RL) and natural language processing (NLP). The application also integrates with Google Calendar for scheduling and includes user authentication features like login and registration.

The AI Study Planner leverages reinforcement learning to optimize study schedules based on user inputs such as subjects, deadlines, and available hours per day. It also uses NLP to parse subjects/topics and provides a clean interface to track progress and sync schedules with Google Calendar.

## Features

- **User Authentication**: Secure login and registration system for users to manage their study plans.
- **Study Plan Generation**: Generate personalized study plans using a reinforcement learning algorithm based on subjects, deadlines, and available hours.
- **Natural Language Processing (NLP)**: Parse subjects/topics using spaCy for smarter input processing (with a fallback for simple comma-separated parsing).
- **Progress Tracking**: Track and mark completed tasks within your study plan.
- **Google Calendar Integration**: Sync your study plan with Google Calendar for seamless scheduling.
- **Responsive Design**: A clean and responsive UI built with Tailwind CSS and custom styles.
- **Dynamic UI Updates**: Real-time updates to the study plan and error handling using JavaScript and AJAX.

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS (Tailwind CSS), JavaScript
- **Database**: SQLite (via Flask-SQLAlchemy)
- **Machine Learning**: Reinforcement Learning (custom implementation with NumPy)
- **NLP**: spaCy for subject parsing
- **APIs**: Google Calendar API for event scheduling
- **Security**: Werkzeug for password hashing, Flask-Login for user session management
- **Styling**: Tailwind CSS and custom CSS

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- A Google Cloud project with the Calendar API enabled (for Google Calendar integration)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/ai-study-planner.git
   cd ai-study-planner
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   If a `requirements.txt` file doesn't exist, you can install the required packages manually:
   ```bash
   pip install flask flask-sqlalchemy flask-login spacy google-auth-oauthlib google-api-python-client numpy
   ```

4. **Download the spaCy Model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Set Up Google Calendar API**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a project and enable the Google Calendar API.
   - Download the `credentials.json` file and place it in the project root.
   - The app will generate a `token.pickle` file after the first successful authentication.

6. **Configure Environment Variables**:
   Create a `.env` file or set environment variables for sensitive data:
   ```bash
   export SECRET_KEY='your-secret-key'  # Replace with a secure key
   export GOOGLE_CLIENT_ID='your-client-id'
   export GOOGLE_CLIENT_SECRET='your-client-secret'
   ```

7. **Initialize the Database**:
   Run the Flask app once to create the SQLite database:
   ```bash
   python app.py
   ```

8. **Run the Application**:
   ```bash
   python app.py
   ```
   The app will be accessible at `http://127.0.0.1:5000`.

## Usage

1. **Register and Login**:
   - Navigate to `/register` to create a new account.
   - Use `/login` to access your account with your username and password.
   - Passwords are securely hashed using `pbkdf2:sha256`.

2. **Create a Study Plan**:
   - After logging in, go to the homepage (`/`).
   - Enter your subjects/topics (comma-separated or natural language), deadline, and available hours per day.
   - Click "Generate Study Plan" to create a schedule using reinforcement learning.

3. **Track Progress**:
   - View your saved plans on the homepage.
   - Click "View Progress" to track completed tasks and mark them as done.

4. **Sync with Google Calendar**:
   - Click "Sync with Google Calendar" to add your study plan events to your calendar.
   - Authenticate with Google when prompted.

## Project Structure

```
ai-study-planner/
├── app.py                    # Main Flask application
├── config.py                 # Configuration settings
├── rl_model.py               # Reinforcement Learning model for scheduling
├── models.py                 # Database models (User, StudyPlan, Progress)
├── static/
│   ├── css/
│   │   └── styles.css        # Custom CSS styles
│   └── js/
│       └── script.js         # Frontend JavaScript logic
├── templates/
│   ├── base.html             # Base HTML template
│   ├── index.html            # Homepage template
│   ├── login.html            # Login page template
│   ├── register.html         # Registration page template
│   └── progress.html         # Progress tracking template
└── database.db               # SQLite database (not tracked)
```
## Future Improvements

- Add more advanced RL algorithms for better scheduling.
- Support for multiple deadlines and priority-based scheduling.
- Enhance NLP capabilities for more complex subject parsing.
- Add user notifications for upcoming study sessions.
- Implement a dashboard with analytics on study progress.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure your code follows the project's style guidelines and includes tests where applicable.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/) for the web framework.
- [spaCy](https://spacy.io/) for NLP capabilities.
- [Google Calendar API](https://developers.google.com/calendar) for calendar integration.
- [Tailwind CSS](https://tailwindcss.com/) for styling.
