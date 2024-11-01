import logging
from flask import Flask
from flask_cors import CORS
from routes import routes

app = Flask(__name__)

CORS(app)

# Set up basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler("backend.log"),  # Log to file
    ],
)

# Get a logger instance
logger = logging.getLogger(__name__)

# Register blueprints
app.register_blueprint(routes)

@app.route("/")
def home():
    logger.info("Attachment route accessed.")
    return "Attachment Service is running!"


if __name__ == "__main__":
    logger.info("Starting the attachment service...")
    try:
        app.run(host="0.0.0.0", port=5001)
        logger.info("Attachment service started successfully!")
    except Exception as e:
        logger.error(f"Error starting attachment service: {str(e)}")