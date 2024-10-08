import React, { useState } from 'react';

const ATTACHMENTS_BACKEND_BASE_URL = "http://localhost:5001/participants";

const Attachments = () => {
    const handleCreateAttachment = () => {
    };

    const handleAttachmentDisplay = () => {
    }

    const handleFindAttachment = () => {
    }

    const handleShowDeleteAttachment = () => {
    }

    const handleShowUpdateAttachment = () => {
    }


    return (
        <div>
            <button onClick={handleCreateAttachment}>Create Attachment</button>
            <button onClick={handleAttachmentDisplay}>Display Attachments</button>
            <button onClick={handleFindAttachment}>Find Attachment</button>
            <button onClick={handleShowDeleteAttachment}>Delete Attachment</button>
            <button onClick={handleShowUpdateAttachment}>Update Attachment</button>
        </div>
    )
}

export default Attachments;
