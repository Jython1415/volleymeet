import React, { useState } from 'react';

const PARTICIPANTS_BACKEND_BASE_URL = "http://localhost:5001/participants"; // Your backend URL

const FindParticipantForm = ({ onFindParticipant }) => {
    const [participantId, setParticipantId] = useState('');

    const handleChange = (e) => {
        setParticipantId(e.target.value);
    };

    const handleFindParticipant = (e) => {
        e.preventDefault();
        onFindParticipant(participantId);  // Call the parent function to find the participant
    };

    return (
        <div>
            <h3>Find Participant</h3>
            <form onSubmit={handleFindParticipant}>
                <label>Participant ID:</label>
                <input
                    type="text"
                    name="participant_id"
                    value={participantId}
                    onChange={handleChange}
                    required
                />
                <button type="submit">Find Participant</button>
            </form>
        </div>
    );
};

export default FindParticipantForm;
