import React, { useState } from 'react';
import ParticipantList from './ParticipantList';
import CreateParticipantForm from './CreateParticipantForm';
import FindParticipantForm from './FindParticipantForm';

const PARTICIPANTS_BACKEND_BASE_URL = "http://localhost:5001/participants";

const Participants = () => {
    const [participants, setParticipants] = useState([]);
    const [showCreateParticipantForm, setShowCreateParticipantForm] = useState(false);
    const [showParticipantList, setShowParticipantList] = useState(false);
    const [showFindParticipantForm, setShowFindParticipantForm] = useState(false);

    const [responseMessage, setResponseMessage] = useState('');
    const [error, setError] = useState('');


    // Helper function to reset all form visibility states
    const resetFormVisibility = () => {
        setShowCreateParticipantForm(false);
        setShowParticipantList(false);
        setShowFindParticipantForm(false);
        setResponseMessage('');
        setError('');

    }

    const handleCreateParticipant = () => {
        resetFormVisibility();
        setShowCreateParticipantForm(true);
    };

    const handleParticipantDisplay = async () => {
        resetFormVisibility();
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
        resetFormVisibility();
        setShowFindParticipantForm(true);
    }

    const handleShowDeleteParticipant = () => {
    }

    const handleShowUpdateParticipant = () => {
    }

    const handleFindParticipantById = async (participantId) => {
        try {
            const response = await fetch(`${PARTICIPANTS_BACKEND_BASE_URL}/${participantId}`);
            if (response.status === 200) {
                const participant = await response.json();
                setParticipants([participant]);
                setShowParticipantList(true);
            } else if (response.status === 404) {
                setError("Participant not found.");
            } else {
                setError(`Failed to fetch participant with status code ${response.status}`);
            }
        } catch (err) {
            setError('Error fetching the participant.');
        }
    };


    return (
        <div>
            <button onClick={handleCreateParticipant}>Create Participant</button>
            <button onClick={handleParticipantDisplay}>Display Participants</button>
            <button onClick={handleFindParticipant}>Find Participant</button>
            <button onClick={handleShowDeleteParticipant}>Delete Participant</button>
            <button onClick={handleShowUpdateParticipant}>Update Participant</button>

            {showCreateParticipantForm && <CreateParticipantForm />}
            {showParticipantList && <ParticipantList participants={participants} />}
            {showFindParticipantForm && <FindParticipantForm onFindParticipant={handleFindParticipantById} />}

            {responseMessage && <p>{responseMessage}</p>}
            {error && <p>{error}</p>}
        </div>
    )
}

export default Participants;
