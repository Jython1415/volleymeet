import React, { useState } from 'react';

const BACKEND_BASE_URL = "http://localhost:5001/attachments"; // Backend URL for attachments

const AddAttachmentForm = ({ meetingId, onSubmit }) => {
  const [attachment, setAttachment] = useState({
    attachment_id: '', // Generate a UUID if not provided
    meeting_id: meetingId,
    attachment_url: ''
  });

  const [responseMessage, setResponseMessage] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setAttachment({ ...attachment, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const attachmentData = {
      attachment_id: attachment.attachment_id || uuidv4(), // Generate a new UUID if missing
      meeting_id: attachment.meeting_id,
      attachment_url: attachment.attachment_url,
    };

    try {
      const response = await fetch(BACKEND_BASE_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(attachmentData),
      });

      if (response.status === 201) {
        setResponseMessage('Attachment added successfully!');
        onSubmit(attachmentData); // Pass the new attachment back to the parent
        setAttachment({ ...attachment, attachment_url: '' }); // Reset the URL input field
      } else {
        const result = await response.json();
        setResponseMessage(`Failed to add attachment: ${result.error || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Error adding attachment:', error);
      setResponseMessage('Error adding attachment. Please try again.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>Attachment ID:</label>
      <input type="text" name="attachment_id" value={attachment.attachment_id} readOnly />

      <label>Meeting ID:</label>
      <input type="text" name="meeting_id" value={attachment.meeting_id} readOnly />

      <label>Attachment URL:</label>
      <input type="text" name="attachment_url" value={attachment.attachment_url} onChange={handleChange} required />

      <button type="submit">Add Attachment</button>
      {responseMessage && <p>{responseMessage}</p>}
    </form>
  );
};

export default AddAttachmentForm;
