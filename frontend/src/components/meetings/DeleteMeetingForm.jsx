import React, { useState } from 'react';

const MEETINGS_BACKEND_BASE_URL = "http://localhost:5004";

const DeleteMeetingForm = ({ onDeleteMeeting }) => {
    const [meetingId, setMeetingId] = useState('');

    const handleChange = (e) => {
        setMeetingId(e.target.value);
    };

    const handleDeleteMeeting = (e) => {
        e.preventDefault();
        onDeleteMeeting(meetingId); // Call the delete function from props
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
