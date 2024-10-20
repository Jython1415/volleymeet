import React, { useState } from 'react';

const BASE_URL = "http://localhost:80";
const MEETINGS_BACKEND_BASE_URL = `${BASE_URL}/meetings`;

const UpdateMeetingForm = () => {
    const [meeting, setMeeting] = useState({
        id: '',
        title: '',
        date_time: '',
        location: '',
        details: '',
    });

    const [responseMessage, setResponseMessage] = useState('');


    const handleUpdateMeeting = async (e) => {
        e.preventDefault();

        const meetingData = {
            meeting_id: meeting.meeting_id || undefined, // Allow meeting_id to be optional
            title: meeting.title,
            date_time: meeting.date_time,
            location: meeting.location,
            details: meeting.details,
        };

        try {
            const response = await fetch(`${MEETINGS_BACKEND_BASE_URL}/${meeting.meeting_id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(meetingData),
            });

            if (response.status === 200) {
                setResponseMessage('Meeting updated successfully!');
                setMeeting({ meeting_id: '', title: '', date_time: '', location: '', details: '' }); // Reset form
            } else {
                const result = await response.json();
                setResponseMessage(`Failed to update meeting: ${result.error || 'Unknown error'}`);
            }
        } catch (error) {
            console.error('Error updating meeting:', error);
            setResponseMessage('Error updating meeting. Please try again.');
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setMeeting({ ...meeting, [name]: value });
    };

    return (
        <div>
            {/* Update Meeting Form */}
            <h3>Update Meeting</h3>
            <form onSubmit={handleUpdateMeeting}>
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
        </div>
    )
}

export default UpdateMeetingForm;
