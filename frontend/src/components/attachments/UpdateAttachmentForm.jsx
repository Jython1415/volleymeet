import React, { useState } from 'react';

const ATTACHMENTS_BACKEND_BASE_URL = "http://localhost:5001/attachments";

const UpdateAttachmentForm = () => {
    const [attachment, setAttachment] = useState({
        id: '',
        meeting_id: '',
        attachment_url: '',
    });

    const [responseMessage, setResponseMessage] = useState('');


    const handleUpdateAttachment = async (e) => {
        e.preventDefault();

        const attachmentData = {
            attachment_id: attachment.attachment_id || undefined, // Allow attachment_id to be optional
            meeting_id: attachment.meeting_id,
            attachment_url: attachment.attachment_url,
        };

        try {
            const response = await fetch(`${ATTACHMENTS_BACKEND_BASE_URL}/${attachment.attachment_id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(attachmentData),
            });

            if (response.status === 200) {
                setResponseMessage('Attachment updated successfully!');
                setAttachment({ attachment_id: '', meeting_id: '', attachment_url: '' }); // Reset form
            } else {
                const result = await response.json();
                setResponseMessage(`Failed to update attachment: ${result.error || 'Unknown error'}`);
            }
        } catch (error) {
            console.error('Error updating attachment:', error);
            setResponseMessage('Error updating attachment. Please try again.');
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setAttachment({ ...attachment, [name]: value });
    };

    return (
        <div>
            {/* Update Attachment Form */}
            <h3>Update Attachment</h3>
            <form onSubmit={handleUpdateAttachment}>
                <label>Attachment ID:</label>
                <input type="text" name="attachment_id" value={attachment.attachment_id} onChange={handleChange} />

                <label>Meeting Id:</label>
                <input type="text" name="name" value={attachment.meeting_id} onChange={handleChange} required />

                <label>Attachment Url:</label>
                <input type="text" name="email" value={attachment.attachment_url} onChange={handleChange} required />

                <button type="submit">Submit</button>
                {responseMessage && <p>{responseMessage}</p>} {/* Display response message */}
            </form>
        </div>
    )
}

export default UpdateAttachmentForm;
