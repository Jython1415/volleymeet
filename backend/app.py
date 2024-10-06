from flask import Flask, jsonify, request
from meetings_sql_queries import (
    create_meeting,
    get_all_meetings,
    get_meeting_by_id,
    update_meeting,
    delete_meeting,
)

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, Flask!"


# Endpoint to get all meetings
@app.route("/meetings", methods=["GET"])
def api_get_meetings():
    meetings = get_all_meetings()
    return jsonify(meetings)


# Endpoint to get a specific meeting by ID
@app.route("/meetings/<meeting_id>", methods=["GET"])
def api_get_meeting(meeting_id):
    meeting = get_meeting_by_id(meeting_id)
    return jsonify(meeting)


# Endpoint to add a new meeting
@app.route("/meetings", methods=["POST"])
def api_add_meeting():
    data = request.get_json()
    title = data.get("title")
    date_time = data.get("date_time")
    location = data.get("location")
    details = data.get("details")
    meeting_id = data.get("meeting_id")

    try:
        create_meeting(title, date_time, location, details, meeting_id)
        return ("Created", 201)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# Endpoint to update an existing meeting
@app.route("/meetings/<meeting_id>", methods=["PUT"])
def api_update_meeting(meeting_id):
    data = request.get_json()
    title = data.get("title")
    date_time = data.get("date_time")
    location = data.get("location")
    details = data.get("details")

    try:
        update_meeting(meeting_id, title, date_time, location, details)
        return ("Updated", 200)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# Endpoint to delete a meeting by ID
@app.route("/meetings/<meeting_id>", methods=["DELETE"])
def api_delete_meeting(meeting_id):
    delete_meeting(meeting_id)
    return ("Deleted", 204)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
