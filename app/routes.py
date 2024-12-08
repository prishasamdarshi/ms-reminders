from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models import Reminder, db
from app.utils import send_email
from sqlalchemy.sql import text
import json

reminder_bp = Blueprint('reminder', __name__)


@reminder_bp.route("/", methods=["GET"])
def home():
    """
    Welcome Route
    ---
    responses:
      200:
        description: Welcome message for the Reminders Microservice
    """
    return "Welcome to the Reminders Microservice"


@reminder_bp.route('/reminders', methods=['POST'])
def create_reminder():
    """
    Create a new reminder
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            task_id:
              type: integer
            user_id:
              type: integer
            reminder_time:
              type: string
              format: date
            message:
              type: string
    responses:
      201:
        description: Reminder created successfully
    """
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
    """
    Get a reminder by ID
    ---
    parameters:
      - name: reminder_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Reminder details
        schema:
          type: object
          properties:
            id:
              type: integer
            task_id:
              type: integer
            user_id:
              type: integer
            reminder_time:
              type: string
              format: date
            message:
              type: string
      404:
        description: Reminder not found
    """
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
