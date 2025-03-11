import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your secret key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_CLIENT_ID = 'your client id'
    GOOGLE_CLIENT_SECRET = 'client secret'