// LinkParticipantForm.jsx
import React, { useState } from 'react';

const LinkParticipantForm = ({ onLinkParticipant }) => {
    const [participantId, setParticipantId] = useState('');
    const [meetingId, setMeetingId] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        onLinkParticipant(meetingId, participantId);
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label>Meeting ID:</label>
                <input
                    type="text"
                    value={meetingId}
                    onChange={(e) => setMeetingId(e.target.value)}
                    required
                />
            </div>
            <div>
                <label>Participant ID:</label>
                <input
                    type="text"
                    value={participantId}
                    onChange={(e) => setParticipantId(e.target.value)}
                    required
                />
            </div>
            <button type="submit">Link Participant</button>
        </form>
    );
};

export default LinkParticipantForm;
