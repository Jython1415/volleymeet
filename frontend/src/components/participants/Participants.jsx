import React, { useState } from 'react';

const PARTICIPANTS_BACKEND_BASE_URL = "http://localhost:5001/participants";

const Participants = () => {
    const handleCreateParticipant = () => {
    };

    const handleParticipantDisplay = () => {
    }

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
        </div>
    )
}

export default Participants;
