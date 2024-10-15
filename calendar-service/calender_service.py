from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://calendar_user:calendarpassword@localhost:3307/calendar_db'
db = SQLAlchemy(app)

class Calendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    details = db.Column(db.Text)
    meeting_ids = db.Column(db.Text)  # Storing Meeting IDs as a comma-separated list

db.create_all()

@app.route('/calendars', methods=['POST'])
def create_calendar():
    data = request.json
    calendar = Calendar(title=data['title'], details=data['details'], meeting_ids=','.join(data['meeting_ids']))
    db.session.add(calendar)
    db.session.commit()
    return jsonify({"id": calendar.id}), 201

@app.route('/calendars/<id>', methods=['GET'])
def get_calendar(id):
    calendar = Calendar.query.get(id)
    if not calendar:
        return jsonify({'error': 'Calendar not found'}), 404
    return jsonify({
        'id': calendar.id,
        'title': calendar.title,
        'details': calendar.details,
        'meeting_ids': calendar.meeting_ids.split(',')
    })

@app.route('/calendars', methods=['GET'])
def list_calendars():
    calendars = Calendar.query.all()
    return jsonify([{
        'id': c.id, 'title': c.title, 'details': c.details, 'meeting_ids': c.meeting_ids.split(',')
    } for c in calendars])

@app.route('/calendars/<id>', methods=['PUT'])
def update_calendar(id):
    data = request.json
    calendar = Calendar.query.get(id)
    if not calendar:
        return jsonify({'error': 'Calendar not found'}), 404
    calendar.title = data.get('title', calendar.title)
    calendar.details = data.get('details', calendar.details)
    calendar.meeting_ids = ','.join(data.get('meeting_ids', calendar.meeting_ids.split(',')))
    db.session.commit()
    return jsonify({"message": "Calendar updated successfully"})

@app.route('/calendars/<id>', methods=['DELETE'])
def delete_calendar(id):
    calendar = Calendar.query.get(id)
    if not calendar:
        return jsonify({'error': 'Calendar not found'}), 404
    db.session.delete(calendar)
    db.session.commit()
    return jsonify({"message": "Calendar deleted successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
