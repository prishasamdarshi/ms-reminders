from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models import Reminder, db
from app.utils import send_email
from sqlalchemy.sql import text
import json

reminder_bp = Blueprint('reminder', __name__)


@reminder_bp.route('/reminders', methods=['POST'])
def create_reminder():
    data = request.json
    reminder = Reminder(
        task_id=data['task_id'],
        user_id=data['user_id'],
        reminder_time=datetime.strptime(data['reminder_time'], "%Y-%m-%d"),
        message=data.get('message', '')
    )
    db.session.add(reminder)
    db.session.commit()
    return jsonify({'id': reminder.id, 'message': 'Reminder created successfully'}), 201


@reminder_bp.route('/reminders/<int:reminder_id>', methods=['GET'])
def get_reminder(reminder_id):
    reminder = Reminder.query.get(reminder_id)
    if not reminder:
        return jsonify({'error': 'Reminder not found'}), 404
    return jsonify({
        'id': reminder.id,
        'task_id': reminder.task_id,
        'user_id': reminder.user_id,
        'reminder_time': reminder.reminder_time,
        'message': reminder.message
    })


@reminder_bp.route('/reminders/<int:reminder_id>', methods=['PUT'])
def edit_reminder(reminder_id):
    data = request.json
    reminder = Reminder.query.get(reminder_id)
    if not reminder:
        return jsonify({'error': 'Reminder not found'}), 404
    reminder.reminder_time = datetime.strptime(
        data['reminder_time'], "%Y-%m-%d")
    reminder.message = data.get('message', reminder.message)
    db.session.commit()
    return jsonify({'message': 'Reminder updated successfully'})


@reminder_bp.route('/reminders/<int:reminder_id>', methods=['DELETE'])
def delete_reminder(reminder_id):
    reminder = Reminder.query.get(reminder_id)
    if not reminder:
        return jsonify({'error': 'Reminder not found'}), 404
    db.session.delete(reminder)
    db.session.commit()
    return jsonify({'message': 'Reminder deleted successfully'})


@reminder_bp.route('/notifications', methods=['POST'])
def send_notifications():
    reminders = Reminder.query.filter(
        Reminder.reminder_time == datetime.now().date()
    ).all()
    for reminder in reminders:
        send_email(
            to=f"user_{reminder.user_id}@example.com",
            subject="Reminder Notification",
            body=f"Task ID {reminder.task_id}: {reminder.message}"
        )
    return jsonify({'message': 'Notifications sent successfully'})


@reminder_bp.route('/reminders/grouped', methods=['GET'])
def get_grouped_reminders_mysql():
    """
    Route to group reminders by user using MySQL-compatible JSON functions.
    """
    now = datetime.now().date()
    
    # Raw SQL query for MySQL
    sql_query = text("""
        SELECT 
            user_id,
            JSON_ARRAYAGG(
                JSON_OBJECT(
                    'task_id', task_id,
                    'reminder_time', reminder_time,
                    'message', message
                )
            ) AS tasks
        FROM reminder
        WHERE reminder_time = :reminder_time
        GROUP BY user_id
    """)
    
    result = db.session.execute(sql_query, {'reminder_time': now}).fetchall()
    
    # Parse the JSON strings in `tasks` back into Python objects
    reminders_by_user = [
        {
            'user_id': row.user_id,
            'tasks': json.loads(row.tasks)  # Convert the JSON string to a Python list
        }
        for row in result
    ]
    
    return jsonify({'reminders': reminders_by_user}), 200