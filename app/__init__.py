from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import Config
import logging
import time

db = SQLAlchemy()
mail = Mail()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from app import routes
        from app.models import Reminder
        db.create_all()

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

    return app
