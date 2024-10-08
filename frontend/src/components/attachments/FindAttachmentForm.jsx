import React, { useState } from 'react';

const ATTACHMENTS_BACKEND_BASE_URL = "http://localhost:5001/attachments"; // Your backend URL

const FindAttachmentForm = ({ onFindAttachment }) => {
    const [attachmentId, setAttachmentId] = useState('');

    const handleChange = (e) => {
        setAttachmentId(e.target.value);
    };

    const handleFindAttachment = (e) => {
        e.preventDefault();
        onFindAttachment(attachmentId);  // Call the parent function to find the attachment
    };

    return (
        <div>
            <h3>Find Attachment</h3>
            <form onSubmit={handleFindAttachment}>
                <label>Attachment ID:</label>
                <input
                    type="text"
                    name="attachment_id"
                    value={attachmentId}
                    onChange={handleChange}
                    required
                />
                <button type="submit">Find Attachment</button>
            </form>
        </div>
    );
};

export default FindAttachmentForm;
