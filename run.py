from app import create_app
from app.routes import reminder_bp

app = create_app()
app.register_blueprint(reminder_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)
