import React, { useState } from 'react';

const CALENDARS_BACKEND_BASE_URL = "http://localhost:5002";

const DeleteCalendarForm = ({ onDeleteCalendar }) => {
    const [calendarId, setCalendarId] = useState('');

    const handleChange = (e) => {
        setCalendarId(e.target.value);
    };

    const handleDeleteCalendar = (e) => {
        e.preventDefault();
        onDeleteCalendar(calendarId); // Call the delete function from props
    };

    return (
        <div>
            <h3>Delete Calendar</h3>
            <form onSubmit={handleDeleteCalendar}>
                <label>Calendar ID:</label>
                <input
                    type="text"
                    name="calendar_id"
                    value={calendarId}
                    onChange={handleChange}
                    required
                />
                <button type="submit">Delete Calendar</button>
            </form>
        </div>
    );
};

export default DeleteCalendarForm;
