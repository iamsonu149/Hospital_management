broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/1"
timezone = "Asia/Kolkata"
broker_connection_retry_on_startup = True

from celery.schedules import crontab

beat_schedule = {
    "daily-appointment-reminder": {
        "task": "daily_appointment_reminder",
        "schedule": crontab(),
    },
    "monthly-activity-report": {
    "task": "monthly_activity_report",
    "schedule": crontab(day_of_month=1, hour=7, minute=0),
    },

}
