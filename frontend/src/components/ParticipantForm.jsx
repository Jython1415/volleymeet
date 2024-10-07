import React, { useState } from 'react';

const BACKEND_BASE_URL = "http://localhost:5001/participants"; // Backend URL for participants

const ParticipantForm = ({ meetingId, onSubmit }) => {
  const [participant, setParticipant] = useState({
    participant_id: '', // Generate a UUID if not provided
    meeting_id: meetingId,
    name: '',
    email: ''
  });

  const [responseMessage, setResponseMessage] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setParticipant({ ...participant, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const participantData = {
      participant_id: participant.participant_id || uuidv4(), // Generate a new UUID if missing
      meeting_id: participant.meeting_id,
      name: participant.name,
      email: participant.email,
    };

    try {
      const response = await fetch(BACKEND_BASE_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(participantData),
      });

      if (response.status === 201) {
        setResponseMessage('Participant added successfully!');
        onSubmit(participantData); // Pass the new participant back to the parent
        setParticipant({ ...participant, name: '', email: '' }); // Reset form fields
      } else {
        const result = await response.json();
        setResponseMessage(`Failed to add participant: ${result.error || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Error adding participant:', error);
      setResponseMessage('Error adding participant. Please try again.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>Participant ID:</label>
      <input type="text" name="participant_id" value={participant.participant_id} readOnly />

      <label>Meeting ID:</label>
      <input type="text" name="meeting_id" value={participant.meeting_id} readOnly />

      <label>Participant Name:</label>
      <input type="text" name="name" value={participant.name} onChange={handleChange} required />

      <label>Participant Email:</label>
      <input type="email" name="email" value={participant.email} onChange={handleChange} required />

      <button type="submit">Add Participant</button>
      {responseMessage && <p>{responseMessage}</p>}
    </form>
  );
};

export default ParticipantForm;
