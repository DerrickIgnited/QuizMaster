from celery import Celery
from celery.schedules import crontab
import os
from dotenv import load_dotenv
from tasks.reminders import send_daily_reminders, generate_monthly_report

load_dotenv()

celery = Celery('quiz_master', broker=os.environ.get('REDIS_URL', 'redis://localhost:6379/0'))

# Optional: if using result backend
celery.conf.result_backend = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

# Task schedule (Beat)
celery.conf.beat_schedule = {
    'daily-reminders': {
        'task': 'send_daily_reminders',
        'schedule': crontab(hour=13, minute=35),
        #'schedule': crontab(minute='*/1'),  # every minute for testing
    },
    'monthly-user-report': {
        'task': 'generate_monthly_report',
        'schedule': crontab(day_of_month=1, hour=6, minute=0),
    },
}
