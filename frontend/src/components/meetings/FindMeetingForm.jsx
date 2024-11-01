import React, { useState } from 'react';

const MEETINGS_BACKEND_BASE_URL = "http://localhost:5004";

const FindMeetingForm = ({ onFindMeeting }) => {
    const [meetingId, setMeetingId] = useState('');

    const handleChange = (e) => {
        setMeetingId(e.target.value);
    };

    const handleFindMeeting = (e) => {
        e.preventDefault();
        onFindMeeting(meetingId);  // Call the parent function to find the meeting
    };

    return (
        <div>
            <h3>Find Meeting</h3>
            <form onSubmit={handleFindMeeting}>
                <label>Meeting ID:</label>
                <input
                    type="text"
                    name="meeting_id"
                    value={meetingId}
                    onChange={handleChange}
                    required
                />
                <button type="submit">Find Meeting</button>
            </form>
        </div>
    );
};

export default FindMeetingForm;
