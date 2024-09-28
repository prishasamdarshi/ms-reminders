from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:ms-reminders@reminders-db.cl0ucq86mgcw.us-east-1.rds.amazonaws.com:3306/reminders-db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Register reminders blueprint
from routes.reminders import reminders
app.register_blueprint(reminders)

@app.route('/')
def index():
    return "Reminders Microservice is running!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
