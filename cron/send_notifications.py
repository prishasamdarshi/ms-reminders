from app import create_app, db
from app.models import Reminder
from app.utils import send_email
from datetime import datetime

app = create_app()
app.app_context().push()

reminders = Reminder.query.filter(
    Reminder.reminder_time == datetime.now().date()
).all()

for reminder in reminders:
    send_email(
        to=f"user_{reminder.user_id}@example.com",
        subject="Reminder Notification",
        body=f"Task ID {reminder.task_id}: {reminder.message}"
    )
