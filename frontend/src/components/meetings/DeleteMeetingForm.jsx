import React, { useState } from 'react';

const MEETINGS_BACKEND_BASE_URL = "http://localhost:5001/meetings";

const DeleteMeetingForm = () => {
    const [meetingId, setMeetingId] = useState('');

    const handleChange = (e) => {
        setMeetingId(e.target.value);
    };

    const handleDeleteMeeting = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch(`${MEETINGS_BACKEND_BASE_URL}/${meetingId}`, {
                method: 'DELETE',
            });
            if (response.status === 204) {
                setMeetingId(meetingId.filter((meeting) => meeting.meeting_id !== meetingId));
                setResponseMessage(`Meeting with ID ${meetingId} deleted successfully.`);
            } else if (response.status === 404) {
                setError(`Meeting with ID ${meetingId} not found.`);
            } else {
                setError(`Failed to delete meeting with status code ${response.status}`);
            }
        } catch (err) {
            setError('Error deleting meeting.');
        }

        //onDeleteMeeting(meetingId); // Call the delete function from props
    };

    return (
        <div>
            <h3>Delete Meeting</h3>
            <form onSubmit={handleDeleteMeeting}>
                <label>Meeting ID:</label>
                <input
                    type="text"
                    name="meeting_id"
                    value={meetingId}
                    onChange={handleChange}
                    required
                />
                <button type="submit">Delete Meeting</button>
            </form>
        </div>
    );
};

export default DeleteMeetingForm;
