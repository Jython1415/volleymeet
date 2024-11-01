import { useState } from 'react';

const PARTICIPANTS_BACKEND_BASE_URL = "http://localhost:5005";


const CreateParticipantForm = () => {
    const [participant, setParticipant] = useState({
        id: '',
        name: '',
        email: '',
    });

    const [responseMessage, setResponseMessage] = useState('');

    const handleChange = (e) => {
        const { name, value } = e.target;
        setParticipant({ ...participant, [name]: value });
    };

    const handleAddParticipant = async (e) => {
        e.preventDefault();

        const participantData = {
            ...(participant.participant_id && { participant_id: participant.participant_id }), // Allow participant_id to be optional
            name: participant.name,
            email: participant.email,
        };

        console.log("Participant Data: ", participantData);

        try {
            const response = await fetch(PARTICIPANTS_BACKEND_BASE_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(participantData),
            });

            if (response.status === 201) {
                setResponseMessage('Participant created successfully!');
                setParticipant({ participant_id: '', name: '', email: '' }); // Reset form
            } else {
                const result = await response.json();
                setResponseMessage(`Failed to create participant: ${result.error || 'Unknown error'}`);
            }
        } catch (error) {
            console.error('Error creating participant:', error);
            setResponseMessage('Error creating participant. Please try again.');
        }
    };


    return (
        <div>
            {/* Participant Form */}
            <h3>Create New Participant</h3>
            <form onSubmit={handleAddParticipant}>
                <label>Participant ID (Optional):</label>
                <input type="text" name="participant_id" value={participant.participant_id} onChange={handleChange} placeholder="Leave blank to auto-generate" />

                <label>Name:</label>
                <input type="text" name="name" value={participant.name} onChange={handleChange} required />

                <label>Email:</label>
                <input type="text" name="email" value={participant.email} onChange={handleChange} required />

                <button type="submit">Submit</button>
                {responseMessage && <p>{responseMessage}</p>} {/* Display response message */}
            </form>
        </div>
    );
};

export default CreateParticipantForm;
