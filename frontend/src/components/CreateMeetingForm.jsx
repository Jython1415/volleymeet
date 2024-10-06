import React, { useState } from 'react';
import MeetingFiles from './MeetingFiles';

const BACKEND_BASE_URL = "http://localhost:5001/meetings"; // backend URL

const CreateMeetingForm = ({ onSubmit }) => {
    const [meeting, setMeeting] = useState({
        meeting_id: '',
        title: '',
        dateTime: '',
        location: '',
        details: '',
    });
};

const [responseMessage, setResponseMessage] = useState('');

const handleChange = (e) => {
    const { name, value } = e.target;
    setMeeting({ ...meeting, [name]: value });
};

const handleSubmit = async (e) => {
    e.preventDefault();

    const meetingData = {
        meeting_id: meeting.meeting_id || undefined, // Allow meeting_id to be optional
        title: meeting.title,
        date_time: meeting.dateTime,
        location: meeting.location,
        details: meeting.details,
    };

    try {
        const response = await fetch(BACKEND_BASE_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(meetingData),
        });

        if (response.status === 201) {
            setResponseMessage('Meeting created successfully!');
            onSubmit(); // Optionally call a parent method to refresh the list of meetings
        } else {
            const result = await response.json();
            setResponseMessage(`Failed to create meeting: ${result.error || 'Unknown error'}`);
        }
    } catch (error) {
        console.error('Error creating meeting:', error);
        setResponseMessage('Error creating meeting. Please try again.');
    }
};

return (
    <form onSubmit={handleSubmit}>
        <label>Meeting ID:</label>
        <input type="text" name="id" value={meeting.meeting_id} onChange={handleChange} />

        <label>Date and Time:</label>
        <input type="text" name="dateTime" value={meeting.dateTime} onChange={handleChange} placeholder="YYYY-MM-DD HH:MM AM/PM" />

        <label>Location:</label>
        <input type="text" name="location" value={meeting.location} onChange={handleChange} maxLength="2000" />

        <label>Details:</label>
        <textarea name="details" value={meeting.details} onChange={handleChange} maxLength="10000"></textarea>

        <label>Calendar IDs (comma-separated):</label>
        <input type="text" name="calendarIds" value={meeting.calendarIds} onChange={handleChange} />

        <button type="submit">Submit</button>
    </form>
);

export default CreateMeetingForm;
