from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import send_from_directory

# Import db from models.py
from models import db

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

    @app.route('/')
    def index():
        return "Reminders Microservice is running!"

    @app.route('/ui')
    def serve_ui():
        return send_from_directory('.', 'reminders_ui.html')

    return app




if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

