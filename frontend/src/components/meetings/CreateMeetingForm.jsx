import { useState } from 'react';

const BASE_URL = "http://localhost:80";
const MEETINGS_BACKEND_BASE_URL = `${BASE_URL}/meetings`;
const MEETINGS_BACKEND_BASE_URL = "http://localhost:5004";


const CreateMeetingForm = () => {
    const [meeting, setMeeting] = useState({
        id: '',
        title: '',
        date_time: '',
        location: '',
        details: '',
        calendarIds: [],
        participantIds: [],
        attachmentIds: [],
    });

    const [responseMessage, setResponseMessage] = useState('');

    const handleChange = (e) => {
        const { name, value } = e.target;
        setMeeting({ ...meeting, [name]: value });
    };

    const handleAddMeeting = async (e) => {
        e.preventDefault();

        const meetingData = {
            ...(meeting.meeting_id && { meeting_id: meeting.meeting_id }), // Allow meeting_id to be optional
            title: meeting.title,
            date_time: meeting.date_time,
            location: meeting.location,
            details: meeting.details,
        };

        console.log("Meeting Data: ", meetingData);

        try {
            const response = await fetch(MEETINGS_BACKEND_BASE_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(meetingData),
            });

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
        <div>
            {/* Meeting Form */}
            <h3>Create New Meeting</h3>
            <form onSubmit={handleAddMeeting}>
                <label>Meeting ID (Optional):</label>
                <input type="text" name="meeting_id" value={meeting.meeting_id} onChange={handleChange} placeholder="Leave blank to auto-generate" />

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
    );
};

export default CreateMeetingForm;
