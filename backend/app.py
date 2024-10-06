import logging
from flask import Flask
from flask_cors import CORS
from api_routes.meeting_routes import meeting_routes
from api_routes.participant_routes import participant_routes
from api_routes.calendar_routes import calendar_routes
from api_routes.attachment_routes import attachment_routes

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
app.register_blueprint(meeting_routes)
app.register_blueprint(participant_routes)
app.register_blueprint(calendar_routes)
app.register_blueprint(attachment_routes)


@app.route("/")
def home():
    logger.info("Home route accessed.")
    return "Hello, Flask!"


if __name__ == "__main__":
    logger.info("Starting the Flask app...")
    try:
        app.run(host="0.0.0.0", port=5001)
        logger.info("Flask app is running.")
    except Exception as e:
        logger.error(f"Error starting the Flask app: {e}")
