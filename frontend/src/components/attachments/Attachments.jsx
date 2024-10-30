import React, { useState } from 'react';
import AttachmentList from './AttachmentList';
import CreateAttachmentForm from './CreateAttachmentForm';
import FindAttachmentForm from './FindAttachmentForm';
import DeleteAttachmentForm from './DeleteAttachmentForm';
import UpdateAttachmentForm from './UpdateAttachmentForm';

const ATTACHMENTS_BACKEND_BASE_URL = "http://localhost:5001";

const Attachments = () => {
    const [attachments, setAttachments] = useState([]);
    const [showCreateAttachmentForm, setShowCreateAttachmentForm] = useState(false);
    const [showAttachmentList, setShowAttachmentList] = useState(false);
    const [showFindAttachmentForm, setShowFindAttachmentForm] = useState(false);
    const [showDeleteAttachmentForm, setShowDeleteAttachmentForm] = useState(false);
    const [showUpdateAttachmentForm, setShowUpdateAttachmentForm] = useState(false);
    const [responseMessage, setResponseMessage] = useState('');
    const [error, setError] = useState('');


    // Helper function to reset all form visibility states
    const resetFormVisibility = () => {
        setShowCreateAttachmentForm(false);
        setShowAttachmentList(false);
        setShowFindAttachmentForm(false);
        setShowDeleteAttachmentForm(false);
        setShowUpdateAttachmentForm(false);
        setResponseMessage('');
        setError('');

    }

    const handleCreateAttachment = () => {
        resetFormVisibility();
        setShowCreateAttachmentForm(true);
    };

    const handleAttachmentDisplay = async () => {
        resetFormVisibility();
        try {
            // request attachments from the backend ("<base url>/attachments") w/ GET method
            const response = await fetch(`${ATTACHMENTS_BACKEND_BASE_URL}/attachments`, {
                method: 'GET',
            });
            if (response.status === 200) {
                // log the response to the console
                console.log(response);
                const data = await response.json();
                setAttachments(data);
                setShowAttachmentList(true);
            } else if (response.status === 404) {
                setError("No attachments found.");
            } else {
                setError(`Failed to fetch attachments with status code ${response.status}`);
            }
        } catch (err) {
            setError('Error fetching attachments.');
        }
    };

    const handleFindAttachment = () => {
        resetFormVisibility();
        setShowFindAttachmentForm(true);
    }

    const handleShowDeleteAttachment = () => {
        resetFormVisibility();
        setShowDeleteAttachmentForm(true);
    }

    const handleShowUpdateAttachment = () => {
        resetFormVisibility();
        setShowUpdateAttachmentForm(true);
    }

    const handleDeleteAttachment = async (attachmentId) => {
        try {
            const response = await fetch(`${ATTACHMENTS_BACKEND_BASE_URL}/${attachmentId}`, {
                method: 'DELETE',
            });
            if (response.status === 204) {
                setAttachments(attachments.filter((attachment) => attachment.attachment_id !== attachmentId));
                setResponseMessage(`Attachment with ID ${attachmentId} deleted successfully.`);
            } else if (response.status === 404) {
                setError(`Attachment with ID ${attachmentId} not found.`);
            } else {
                setError(`Failed to delete attachment with status code ${response.status}`);
            }
        } catch (err) {
            setError('Error deleting attachment.');
        }
    };

    const handleFindAttachmentById = async (attachmentId) => {
        try {
            const response = await fetch(`${ATTACHMENTS_BACKEND_BASE_URL}/${attachmentId}`, {
                method: 'GET',
            });
            if (response.status === 200) {
                const attachment = await response.json();
                setAttachments([attachment]);
                setShowAttachmentList(true);
            } else if (response.status === 404) {
                setError("Attachment not found.");
            } else {
                setError(`Failed to fetch attachment with status code ${response.status}`);
            }
        } catch (err) {
            setError('Error fetching the attachment.');
        }
    };


    return (
        <div>
            <button onClick={handleCreateAttachment}>Create Attachment</button>
            <button onClick={handleAttachmentDisplay}>Display Attachments</button>
            <button onClick={handleFindAttachment}>Find Attachment</button>
            <button onClick={handleShowDeleteAttachment}>Delete Attachment</button>
            <button onClick={handleShowUpdateAttachment}>Update Attachment</button>

            {showCreateAttachmentForm && <CreateAttachmentForm />}
            {showAttachmentList && <AttachmentList attachments={attachments} />}
            {showFindAttachmentForm && <FindAttachmentForm onFindAttachment={handleFindAttachmentById} />}
            {showDeleteAttachmentForm && <DeleteAttachmentForm onDeleteAttachment={handleDeleteAttachment} />}
            {showUpdateAttachmentForm && <UpdateAttachmentForm />}

            {responseMessage && <p>{responseMessage}</p>}
            {error && <p>{error}</p>}
        </div>
    )
}

export default Attachments;
