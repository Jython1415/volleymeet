import React, { useState } from 'react';

const LinkCalendarForm = ({ onLinkCalendar }) => {
    const [meetingId, setMeetingId] = useState('');
    const [calendarId, setCalendarId] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (meetingId && calendarId) {
            onLinkCalendar(meetingId, calendarId);
        } else {
            alert('Both Meeting ID and Calendar ID are required.');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label htmlFor="meetingId">Meeting ID:</label>
                <input
                    type="text"
                    id="meetingId"
                    value={meetingId}
                    onChange={(e) => setMeetingId(e.target.value)}
                    required
                />
            </div>
            <div>
                <label htmlFor="calendarId">Calendar ID:</label>
                <input
                    type="text"
                    id="calendarId"
                    value={calendarId}
                    onChange={(e) => setCalendarId(e.target.value)}
                    required
                />
            </div>
            <button type="submit">Link Calendar</button>
        </form>
    );
};

export default LinkCalendarForm;
