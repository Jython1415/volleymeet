from flask import Flask
from api_routes.meeting_routes import meeting_routes
from api_routes.participant_routes import participant_routes
from api_routes.calendar_routes import calendar_routes

app = Flask(__name__)

# Register blueprints
app.register_blueprint(meeting_routes)
app.register_blueprint(participant_routes)
app.register_blueprint(calendar_routes)


@app.route("/")
def home():
    return "Hello, Flask!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
