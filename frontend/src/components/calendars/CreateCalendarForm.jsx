import { useState } from 'react';

const CALENDARS_BACKEND_BASE_URL = "http://localhost:5001/calendars";


const CreateCalendarForm = () => {
    const [calendar, setCalendar] = useState({
        id: '',
        title: '',
        details: '',
    });

    const [responseMessage, setResponseMessage] = useState('');

    const handleChange = (e) => {
        const { name, value } = e.target;
        setCalendar({ ...calendar, [name]: value });
    };

    const handleAddCalendar = async (e) => {
        e.preventDefault();

        const calendarData = {
            ...(calendar.calendar_id && { calendar_id: calendar.calendar_id }), // Allow calendar_id to be optional
            title: calendar.title,
            details: calendar.details,
        };

        console.log("Calendar Data: ", calendarData);

        try {
            const response = await fetch(CALENDARS_BACKEND_BASE_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(calendarData),
            });

            if (response.status === 201) {
                setResponseMessage('Calendar created successfully!');
                setCalendar({ calendar_id: '', title: '', details: '' }); // Reset form
            } else {
                const result = await response.json();
                setResponseMessage(`Failed to create calendar: ${result.error || 'Unknown error'}`);
            }
        } catch (error) {
            console.error('Error creating calendar:', error);
            setResponseMessage('Error creating calendar. Please try again.');
        }
    };


    return (
        <div>
            {/* Calendar Form */}
            <h3>Create New Calendar</h3>
            <form onSubmit={handleAddCalendar}>
                <label>Calendar ID (Optional):</label>
                <input type="text" name="calendar_id" value={calendar.calendar_id} onChange={handleChange} placeholder="Leave blank to auto-generate" />

                <label>Title:</label>
                <input type="text" name="title" value={calendar.title} onChange={handleChange} required />

                <label>Details:</label>
                <textarea name="details" value={calendar.details} onChange={handleChange} maxLength="10000"></textarea>

                <button type="submit">Submit</button>
                {responseMessage && <p>{responseMessage}</p>} {/* Display response message */}
            </form>
        </div>
    );
};

export default CreateCalendarForm;
