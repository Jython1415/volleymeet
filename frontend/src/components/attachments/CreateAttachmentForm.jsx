import { useState } from 'react';

const ATTACHMENTS_BACKEND_BASE_URL = "http://localhost:5001/attachments";


const CreateAttachmentForm = () => {
    const [attachment, setAttachment] = useState({
        id: '',
        meeting_id: '',
        attachment_url: '',
    });

    const [responseMessage, setResponseMessage] = useState('');

    const handleChange = (e) => {
        const { name, value } = e.target;
        setAttachment({ ...attachment, [name]: value });
    };

    const handleAddAttachment = async (e) => {
        e.preventDefault();

        const attachmentData = {
            ...(attachment.attachment_id && { attachment_id: attachment.attachment_id }), // Allow attachment_id to be optional
            meeting_id: attachment.meeting_id,
            attachment_url: attachment.attachment_url,
        };

        console.log("Attachment Data: ", attachmentData);

        try {
            const response = await fetch(ATTACHMENTS_BACKEND_BASE_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(attachmentData),
            });

            if (response.status === 201) {
                setResponseMessage('Attachment created successfully!');
                setAttachment({ attachment_id: '', meeting_id: '', attachment_url: '' }); // Reset form
            } else {
                const result = await response.json();
                setResponseMessage(`Failed to create attachment: ${result.error || 'Unknown error'}`);
            }
        } catch (error) {
            console.error('Error creating attachment:', error);
            setResponseMessage('Error creating attachment. Please try again.');
        }
    };


    return (
        <div>
            {/* Attachment Form */}
            <h3>Create New Attachment</h3>
            <form onSubmit={handleAddAttachment}>
                <label>Attachment ID (Optional):</label>
                <input type="text" name="attachment_id" value={attachment.attachment_id} onChange={handleChange} placeholder="Leave blank to auto-generate" />

                <label>Meeting ID:</label>
                <input type="text" name="name" value={attachment.meeting_id} onChange={handleChange} required />

                <label>Attachment Url:</label>
                <input type="text" name="email" value={attachment.attachment_url} onChange={handleChange} required />

                <button type="submit">Submit</button>
                {responseMessage && <p>{responseMessage}</p>} {/* Display response message */}
            </form>
        </div>
    );
};

export default CreateAttachmentForm;
