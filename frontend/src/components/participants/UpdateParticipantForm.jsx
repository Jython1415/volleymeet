import React, { useState } from 'react';

const BASE_URL = "http://localhost:80";
const PARTICIPANTS_BACKEND_BASE_URL = `${BASE_URL}/participants`;
// const PARTICIPANTS_BACKEND_BASE_URL = "http://localhost:5005";

const UpdateParticipantForm = () => {
    const [participant, setParticipant] = useState({
        id: '',
        name: '',
        email: '',
    });

    const [responseMessage, setResponseMessage] = useState('');


    const handleUpdateParticipant = async (e) => {
        e.preventDefault();

        const participantData = {
            participant_id: participant.participant_id || undefined, // Allow participant_id to be optional
            name: participant.name,
            email: participant.email,
        };

        try {
            const response = await fetch(`${PARTICIPANTS_BACKEND_BASE_URL}/${participant.participant_id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(participantData),
            });

            if (response.status === 200) {
                setResponseMessage('Participant updated successfully!');
                setParticipant({ participant_id: '', name: '', email: '' }); // Reset form
            } else {
                const result = await response.json();
                setResponseMessage(`Failed to update participant: ${result.error || 'Unknown error'}`);
            }
        } catch (error) {
            console.error('Error updating participant:', error);
            setResponseMessage('Error updating participant. Please try again.');
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setParticipant({ ...participant, [name]: value });
    };

    return (
        <div>
            {/* Update Participant Form */}
            <h3>Update Participant</h3>
            <form onSubmit={handleUpdateParticipant}>
                <label>Participant ID:</label>
                <input type="text" name="participant_id" value={participant.participant_id} onChange={handleChange} />

                <label>Name:</label>
                <input type="text" name="name" value={participant.name} onChange={handleChange} required />

                <label>Email:</label>
                <input type="text" name="email" value={participant.email} onChange={handleChange} required />

                <button type="submit">Submit</button>
                {responseMessage && <p>{responseMessage}</p>} {/* Display response message */}
            </form>
        </div>
    )
}

export default UpdateParticipantForm;
