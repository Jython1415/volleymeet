import React, { useState } from 'react';

const CALENDARS_BACKEND_BASE_URL = "http://localhost:5002";

const UpdateCalendarForm = () => {
    const [calendar, setCalendar] = useState({
        id: '',
        title: '',
        details: '',
    });

    const [responseMessage, setResponseMessage] = useState('');


    const handleUpdateCalendar = async (e) => {
        e.preventDefault();

        const calendarData = {
            calendar_id: calendar.calendar_id || undefined, // Allow calendar_id to be optional
            title: calendar.title,
            details: calendar.details,
        };

        try {
            const response = await fetch(`${CALENDARS_BACKEND_BASE_URL}/${calendar.calendar_id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(calendarData),
            });

            if (response.status === 200) {
                setResponseMessage('Calendar updated successfully!');
                setCalendar({ calendar_id: '', title: '', details: '' }); // Reset form
            } else {
                const result = await response.json();
                setResponseMessage(`Failed to update calendar: ${result.error || 'Unknown error'}`);
            }
        } catch (error) {
            console.error('Error updating calendar:', error);
            setResponseMessage('Error updating calendar. Please try again.');
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setCalendar({ ...calendar, [name]: value });
    };

    return (
        <div>
            {/* Update Calendar Form */}
            <h3>Update Calendar</h3>
            <form onSubmit={handleUpdateCalendar}>
                <label>Calendar ID:</label>
                <input type="text" name="calendar_id" value={calendar.calendar_id} onChange={handleChange} />

                <label>Title:</label>
                <input type="text" name="title" value={calendar.title} onChange={handleChange} required />

                <label>Details:</label>
                <textarea name="details" value={calendar.details} onChange={handleChange} maxLength="10000"></textarea>

                <button type="submit">Submit</button>
                {responseMessage && <p>{responseMessage}</p>} {/* Display response message */}
            </form>
        </div>
    )
}

export default UpdateCalendarForm;
