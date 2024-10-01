from flask import Blueprint, request, jsonify
from app import db
from datetime import datetime

reminders = Blueprint('reminders', __name__)

# Reminder model
class Reminder(db.Model):
    __tablename__ = 'reminders'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, nullable=False)  # No ForeignKey for testing
    user_id = db.Column(db.Integer, nullable=False)  # No ForeignKey for testing
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

# Initialize the database
@reminders.before_app_request
def create_tables():
    db.create_all()

# Create a new reminder
@reminders.route('/reminders', methods=['POST'])
def create_reminder():
    data = request.get_json()

    # Validate input
    if not data or not data.get('task_id') or not data.get('user_id') or not data.get('reminder_time'):
        return jsonify({'error': 'Missing required fields'}), 400

    # Create new reminder
    new_reminder = Reminder(
        task_id=data['task_id'],
        user_id=data['user_id'],
        reminder_time=datetime.fromisoformat(data['reminder_time']),
        message=data.get('message', ''),
        status=data.get('status', True)
    )

    db.session.add(new_reminder)
    db.session.commit()

    return jsonify({'reminder': new_reminder.to_dict()}), 201

# Get reminders
@reminders.route('/reminders', methods=['GET'])
def get_reminders():
    user_id = request.args.get('user_id')
    task_id = request.args.get('task_id')

    query = Reminder.query

    if user_id:
        query = query.filter_by(user_id=user_id)
    if task_id:
        query = query.filter_by(task_id=task_id)

    reminders = query.all()
    return jsonify([reminder.to_dict() for reminder in reminders]), 200

# Update a reminder
@reminders.route('/reminders/<int:reminder_id>', methods=['PUT'])
def update_reminder(reminder_id):
    data = request.get_json()

    # Find reminder by ID
    reminder = Reminder.query.get(reminder_id)
    if not reminder:
        return jsonify({'error': 'Reminder does not exist'}), 400

    # Update fields
    reminder.reminder_time = datetime.fromisoformat(data.get('reminder_time', reminder.reminder_time.isoformat()))
    reminder.message = data.get('message', reminder.message)
    reminder.status = data.get('status', reminder.status)

    db.session.commit()

    return jsonify({'reminder': reminder.to_dict()}), 200

# Delete a reminder
@reminders.route('/reminders/<int:reminder_id>', methods=['DELETE'])
def delete_reminder(reminder_id):
    reminder = Reminder.query.get(reminder_id)
    if not reminder:
        return jsonify({'error': 'Reminder does not exist'}), 400

    db.session.delete(reminder)
    db.session.commit()

    return jsonify({'message': 'Reminder deleted'}), 200

