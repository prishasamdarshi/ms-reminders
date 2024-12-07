from app import create_app
from app.routes import reminder_bp

app = create_app()
app.register_blueprint(reminder_bp, url_prefix="/api")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

