from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://meeting_user:meetingpassword@localhost:3306/meeting_db'
db = SQLAlchemy(app)

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    date_time = db.Column(db.String(100))
    location = db.Column(db.String(200))
    details = db.Column(db.Text)

db.create_all()

@app.route('/meetings', methods=['POST'])
def create_meeting():
    data = request.json
    meeting = Meeting(title=data['title'], date_time=data['date_time'], location=data['location'], details=data['details'])
    db.session.add(meeting)
    db.session.commit()
    return jsonify({"id": meeting.id}), 201

@app.route('/meetings/<id>', methods=['GET'])
def get_meeting(id):
    meeting = Meeting.query.get(id)
    if not meeting:
        return jsonify({'error': 'Meeting not found'}), 404
    return jsonify({
        'id': meeting.id,
        'title': meeting.title,
        'date_time': meeting.date_time,
        'location': meeting.location,
        'details': meeting.details
    })

@app.route('/meetings', methods=['GET'])
def list_meetings():
    meetings = Meeting.query.all()
    return jsonify([{
        'id': m.id, 'title': m.title, 'date_time': m.date_time, 'location': m.location, 'details': m.details
    } for m in meetings])

@app.route('/meetings/<id>', methods=['PUT'])
def update_meeting(id):
    data = request.json
    meeting = Meeting.query.get(id)
    if not meeting:
        return jsonify({'error': 'Meeting not found'}), 404
    meeting.title = data.get('title', meeting.title)
    meeting.date_time = data.get('date_time', meeting.date_time)
    meeting.location = data.get('location', meeting.location)
    meeting.details = data.get('details', meeting.details)
    db.session.commit()
    return jsonify({"message": "Meeting updated successfully"})

@app.route('/meetings/<id>', methods=['DELETE'])
def delete_meeting(id):
    meeting = Meeting.query.get(id)
    if not meeting:
        return jsonify({'error': 'Meeting not found'}), 404
    db.session.delete(meeting)
    db.session.commit()
    return jsonify({"message": "Meeting deleted successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
