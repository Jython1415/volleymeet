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
    logger.info("Calendar route accessed.")
    return "Calendar Service is running!"


if __name__ == "__main__":
    logger.info("Starting the calendar service...")
    try:
        app.run(host="0.0.0.0", port=5002)
        logger.info("Calendar service started successfully!")
    except Exception as e:
        logger.error(f"Error starting calendar service: {str(e)}")