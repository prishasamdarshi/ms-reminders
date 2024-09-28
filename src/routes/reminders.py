from flask import Blueprint, request, jsonify
from app import db
from datetime import datetime

reminders = Blueprint('reminders', __name__)

class Reminder(db.Model):
    __tablename__ = 'reminders'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.task_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
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


@reminders.route('/reminders', methods=['POST'])
def create_reminder():
    """Create a new reminder for a task"""
    data = request.get_json()

    # Validate requirements
    if not data or not data.get('task_id') or not data.get('user_id') or not data.get('reminder_time'):
        return jsonify({'error': 'Missing required fields'}), 400

    # New reminder object
    new_reminder = Reminder(
        task_id=data['task_id'],
        user_id=data['user_id'],
        reminder_time=datetime.fromisoformat(data['reminder_time']),
        message=data.get('message', ''),
        status = data.get('status', True)
    )

    db.session.add(new_reminder)
    db.session.commit()

    return jsonify({'reminder': new_reminder.to_dict()}), 201


@reminders.route('/reminders', methods=['GET'])
def get_reminders():
    """Get reminder by task_id and user_id"""
    user_id = request.args.get('user_id')
    task_id = request.args.get('task_id')

    query = Reminder.query

    # Filter by user_id if provided
    if user_id:
        query = query.filter_by(user_id=user_id)

    # Filter by task_id if provided
    if task_id:
        query = query.filter_by(task_id=task_id)

    reminders = query.all()

    return jsonify([reminder.to_dict() for reminder in reminders]), 200


@reminders.route('/reminders/<int:reminder_id>', methods=['PUT'])
def update_reminder(reminder_id):
    """Update a reminder by id"""
    data = request.get_json()

    # Find reminder by reminder_id
    reminder = Reminder.query.get(reminder_id)
    if not reminder:
        return jsonify({'error': 'Reminder does not exist'}), 400

    reminder.reminder_time = datetime.fromisoformat(data.get('reminder_time', reminder.reminder_time.isoformat()))
    reminder.message = data.get('message', reminder.message)
    reminder.status = data.get('status', reminder.status)

    db.session.commit()

    return jsonify({'reminder': reminder.to_dict()}), 200


@reminders.route('/reminders/<int:reminder_id>', methods=['DELETE'])
def delete_reminder(reminder_id):
    """Delete a reminder by reminder_id"""
    reminder = Reminder.query.get(reminder_id)
    if not reminder:
        return jsonify({'error': 'Reminder does not exist'}), 400

    db.session.delete(reminder)
    db.session.commit()

    return jsonify({'message': 'Reminder deleted'}), 200

