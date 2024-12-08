from flask import Flask
from flasgger import Swagger
from app import create_app
from app.routes import reminder_bp

app = create_app()
app.register_blueprint(reminder_bp, url_prefix="/api")

# Initialize Swagger
swagger = Swagger(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002, debug=True)
