import React, { useState } from 'react';

const DeleteAttachmentForm = ({ onDeleteAttachment }) => {
    const [attachmentId, setAttachmentId] = useState('');

    const handleChange = (e) => {
        setAttachmentId(e.target.value);
    };

    const handleDeleteAttachment = (e) => {
        e.preventDefault();
        onDeleteAttachment(attachmentId); // Call the delete function from props
    };

    return (
        <div>
            <h3>Delete Attachment</h3>
            <form onSubmit={handleDeleteAttachment}>
                <label>Attachment ID:</label>
                <input
                    type="text"
                    name="attachment_id"
                    value={attachmentId}
                    onChange={handleChange}
                    required
                />
                <button type="submit">Delete Attachment</button>
            </form>
        </div>
    );
};

export default DeleteAttachmentForm;
