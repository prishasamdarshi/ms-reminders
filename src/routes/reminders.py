from flask import Blueprint, request, jsonify
from models import db  # Import db from models
from datetime import datetime

reminders = Blueprint('reminders', __name__)

class Reminder(db.Model):
    __tablename__ = 'reminders'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, nullable=False)  # Removed ForeignKey
    user_id = db.Column(db.Integer, nullable=False)  # Removed ForeignKey
    reminder_time = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.String(255), default='')
    status = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'user_id': self.user_id,
            'reminder_time': self.reminder_time.isoformat(),
            'message': self.message,
            'status': self.status
        }

# Create tables if they do not exist yet
@reminders.before_app_request
def create_tables():
    db.create_all()

