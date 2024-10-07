import React, { useState } from 'react';
import ParticipantForm from './ParticipantForm';
import CalendarForm from './CalendarForm';

const MEETINGS_BACKEND_BASE_URL = "http://localhost:5001/meetings";


const CreateMeetingForm = ({ onSubmit }) => {
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
    const [participants, setParticipants] = useState([]);
    const [calendars, setCalendars] = useState([]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setMeeting({ ...meeting, [name]: value });
    };

    const handleAddMeeting = async (e) => {
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

    const handleAddParticipant = (participantData) => {
        setParticipants([...participants, participantData]);
        setMeeting({
            ...meeting,
            participantIds: [...meeting.participantIds, participantData.participant_id],
        });
    };

    const handleAddCalendar = (calendarData) => {
        setCalendars([...calendars, calendarData]);
        setMeeting({
            ...meeting,
            calendarIds: [...meeting.calendarIds, calendarData.calendar_id],
        });
    };

    return (
        <div>
            {/* Meeting Form */}
            <h3>Create New Meeting</h3>
            <form onSubmit={handleAddMeeting}>
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

            {/* Participant and Calendar Forms */}
            <div className="form-container">
                {/* Participant Section */}
                <div className="participant-section">
                    <h3>Add Participant</h3>
                    <ParticipantForm meetingId={meeting.id} onSubmit={handleAddParticipant} />
                    <h4>Current Participants</h4>
                    <ul>
                        {participants.map(participant => (
                            <li key={participant.participant_id}>
                                {participant.name} - {participant.email}
                            </li>
                        ))}
                    </ul>
                </div>

                {/* Calendar Section */}
                <div className="calendar-section">
                    <h3>Add Calendar</h3>
                    <CalendarForm meetingId={meeting.id} onSubmit={handleAddCalendar} />
                    <h4>Current Calendars</h4>
                    <ul>
                        {calendars.map(calendar => (
                            <li key={calendar.calendar_id}>
                                {calendar.title} - {calendar.details}
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default CreateMeetingForm;
