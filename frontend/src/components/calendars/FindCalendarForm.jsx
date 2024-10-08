import React, { useState } from 'react';

const CALENDARS_BACKEND_BASE_URL = "http://localhost:5001/calendars"; // Your backend URL

const FindCalendarForm = ({ onFindCalendar }) => {
    const [calendarId, setCalendarId] = useState('');

    const handleChange = (e) => {
        setCalendarId(e.target.value);
    };

    const handleFindCalendar = (e) => {
        e.preventDefault();
        onFindCalendar(calendarId);  // Call the parent function to find the calendar
    };

    return (
        <div>
            <h3>Find Calendar</h3>
            <form onSubmit={handleFindCalendar}>
                <label>Calendar ID:</label>
                <input
                    type="text"
                    name="calendar_id"
                    value={calendarId}
                    onChange={handleChange}
                    required
                />
                <button type="submit">Find Calendar</button>
            </form>
        </div>
    );
};

export default FindCalendarForm;
