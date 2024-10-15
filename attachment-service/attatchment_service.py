from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://attachment_user:attachmentpassword@localhost:3309/attachment_db'
db = SQLAlchemy(app)

class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer)  # Foreign key for Meeting ID
    url = db.Column(db.String(500))

db.create_all()

@app.route('/attachments', methods=['POST'])
def create_attachment():
    data = request.json
    attachment = Attachment(meeting_id=data['meeting_id'], url=data['url'])
    db.session.add(attachment)
    db.session.commit()
    return jsonify({"id": attachment.id}), 201

@app.route('/attachments/<id>', methods=['GET'])
def get_attachment(id):
    attachment = Attachment.query.get(id)
    if not attachment:
        return jsonify({'error': 'Attachment not found'}), 404
    return jsonify({
        'id': attachment.id,
        'meeting_id': attachment.meeting_id,
        'url': attachment.url
    })

@app.route('/attachments', methods=['GET'])
def list_attachments():
    attachments = Attachment.query.all()
    return jsonify([{
        'id': a.id, 'meeting_id': a.meeting_id, 'url': a.url
    } for a in attachments])

@app.route('/attachments/<id>', methods=['PUT'])
def update_attachment(id):
    data = request.json
    attachment = Attachment.query.get(id)
    if not attachment:
        return jsonify({'error': 'Attachment not found'}), 404
    attachment.url = data.get('url', attachment.url)
    db.session.commit()
    return jsonify({"message": "Attachment updated successfully"})

@app.route('/attachments/<id>', methods=['DELETE'])
def delete_attachment(id):
    attachment = Attachment.query.get(id)
    if not attachment:
        return jsonify({'error': 'Attachment not found'}), 404
    db.session.delete(attachment)
    db.session.commit()
    return jsonify({"message": "Attachment deleted successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
