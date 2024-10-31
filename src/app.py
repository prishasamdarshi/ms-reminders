import logging
import time
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import send_from_directory

# Import db from models.py
from models import db

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:dbuserdbuser@reminders-db-1.clchno0vc63f.us-east-1.rds.amazonaws.com:3306/reminders_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize db and migrate with the app
    db.init_app(app)
    migrate = Migrate(app, db)

    # Register blueprints
    from routes.reminders import reminders
    app.register_blueprint(reminders)

    # Logging middleware
    @app.before_request
    def log_request_info():
        logger.info(f"Request: {request.method} {request.url}")
        request.start_time = time.time()

    @app.after_request
    def log_response_info(response):
        process_time = time.time() - request.start_time
        logger.info(
            f"Response status: {response.status_code} | Time: {process_time:.4f}s")
        return response

    @app.route('/')
    def index():
        return "Reminders Microservice is running!"

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
