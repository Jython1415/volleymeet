from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://participant_user:participantpassword@localhost:3308/participant_db'
db = SQLAlchemy(app)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    meeting_id = db.Column(db.Integer)  # Foreign key for Meeting ID

db.create_all()

@app.route('/participants', methods=['POST'])
def create_participant():
    data = request.json
    participant = Participant(name=data['name'], email=data['email'], meeting_id=data['meeting_id'])
    db.session.add(participant)
    db.session.commit()
    return jsonify({"id": participant.id}), 201

@app.route('/participants/<id>', methods=['GET'])
def get_participant(id):
    participant = Participant.query.get(id)
    if not participant:
        return jsonify({'error': 'Participant not found'}), 404
    return jsonify({
        'id': participant.id,
        'name': participant.name,
        'email': participant.email,
        'meeting_id': participant.meeting_id
    })

@app.route('/participants', methods=['GET'])
def list_participants():
    participants = Participant.query.all()
    return jsonify([{
        'id': p.id, 'name': p.name, 'email': p.email, 'meeting_id': p.meeting_id
    } for p in participants])

@app.route('/participants/<id>', methods=['PUT'])
def update_participant(id):
    data = request.json
    participant = Participant.query.get(id)
    if not participant:
        return jsonify({'error': 'Participant not found'}), 404
    participant.name = data.get('name', participant.name)
    participant.email = data.get('email', participant.email)
    db.session.commit()
    return jsonify({"message": "Participant updated successfully"})

@app.route('/participants/<id>', methods=['DELETE'])
def delete_participant(id):
    participant = Participant.query.get(id)
    if not participant:
        return jsonify({'error': 'Participant not found'}), 404
    db.session.delete(participant)
    db.session.commit()
    return jsonify({"message": "Participant deleted successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
