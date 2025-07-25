import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'quiz_master_secret_key_2024'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/0'
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
