import React, { useState } from 'react';
import ParticipantList from './ParticipantList';

const PARTICIPANTS_BACKEND_BASE_URL = "http://localhost:5001/participants";

const Participants = () => {
    const [participants, setParticipants] = useState([]);
    const [showParticipantList, setShowParticipantList] = useState(false);

    const [error, setError] = useState('');
    

    // Helper function to reset all form visibility states
    const resetFormVisibility = () => {
        setShowParticipantList(false);
    }

    const handleCreateParticipant = () => {
    };

    const handleParticipantDisplay = async () => {
        resetFormVisibility();
        setError('');
        try {
            const response = await fetch(PARTICIPANTS_BACKEND_BASE_URL);
            if (response.status === 200) {
                const data = await response.json();
                setParticipants(data);
                setShowParticipantList(true);
            } else if (response.status === 404) {
                setError("No participants found.");
            } else {
                setError(`Failed to fetch participants with status code ${response.status}`);
            }
        } catch (err) {
            setError('Error fetching participants.');
        }
    };

    const handleFindParticipant = () => {
    }

    const handleShowDeleteParticipant = () => {
    }

    const handleShowUpdateParticipant = () => {
    }


    return (
        <div>
            <button onClick={handleCreateParticipant}>Create Participant</button>
            <button onClick={handleParticipantDisplay}>Display Participants</button>
            <button onClick={handleFindParticipant}>Find Participant</button>
            <button onClick={handleShowDeleteParticipant}>Delete Participant</button>
            <button onClick={handleShowUpdateParticipant}>Update Participant</button>

            {showParticipantList && <ParticipantList participants={participants} />}

        </div>
    )
}

export default Participants;
