from flask import Flask
from api_routes.meeting_routes import meeting_routes

app = Flask(__name__)

# Register the meeting_routes Blueprint
app.register_blueprint(meeting_routes)


@app.route("/")
def home():
    return "Hello, Flask!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
