import React, { useState } from 'react';

const PARTICIPANTS_BACKEND_BASE_URL = "http://localhost:5005";

const DeleteParticipantForm = ({ onDeleteParticipant }) => {
    const [participantId, setParticipantId] = useState('');

    const handleChange = (e) => {
        setParticipantId(e.target.value);
    };

    const handleDeleteParticipant = (e) => {
        e.preventDefault();
        onDeleteParticipant(participantId); // Call the delete function from props
    };

    return (
        <div>
            <h3>Delete Participant</h3>
            <form onSubmit={handleDeleteParticipant}>
                <label>Participant ID:</label>
                <input
                    type="text"
                    name="participant_id"
                    value={participantId}
                    onChange={handleChange}
                    required
                />
                <button type="submit">Delete Participant</button>
            </form>
        </div>
    );
};

export default DeleteParticipantForm;
