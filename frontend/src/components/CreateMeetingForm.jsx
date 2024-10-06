import React, { useState } from 'react';

const BACKEND_BASE_URL = "http://localhost:5001/meetings"; // backend URL

const CreateMeetingForm = () => {
    const [meeting, setMeeting] = useState({
        meeting_id: '',
        title: '',
        date_time: '',
        location: '',
        details: '',
    });

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
            date_time: meeting.date_time,
            location: meeting.location,
            details: meeting.details,
        };

        console.log("Meeting Data: ", meetingData);

        try {
            const response = await fetch(BACKEND_BASE_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(meetingData),
            });

            console.log(response.)

            if (response.status === 201) {
                setResponseMessage('Meeting created successfully!');
                setMeeting({ meeting_id: '', title: '', date_time: '', location: '', details: '' }); // Reset form
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
            <input type="text" name="meeting_id" value={meeting.meeting_id} onChange={handleChange} />

            <label>Title:</label>
            <input type="text" name="title" value={meeting.title} onChange={handleChange} required />

            <label>Date Time:</label>
            <input
                type="text"
                name="date_time"
                value={meeting.date_time}
                onChange={handleChange}
                placeholder="YYYY-MM-DD HH:MM AM/PM"
                required
            />

            <label>Location:</label>
            <input type="text" name="location" value={meeting.location} onChange={handleChange} maxLength="2000" required />

            <label>Details:</label>
            <textarea name="details" value={meeting.details} onChange={handleChange} maxLength="10000"></textarea>

            <button type="submit">Submit</button>
            {responseMessage && <p>{responseMessage}</p>} {/* Display response message */}
        </form>
    );
};

export default CreateMeetingForm;
