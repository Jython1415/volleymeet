import React, { useState } from 'react';

const BACKEND_BASE_URL = "http://localhost:5001/calendars"; // Backend URL for calendars

const CalendarForm = ({ meetingId, onSubmit }) => {
  const [calendar, setCalendar] = useState({
    calendar_id: '', // Generate a UUID if not provided
    meeting_id: meetingId,
    title: '',
    details: ''
  });

  const [responseMessage, setResponseMessage] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCalendar({ ...calendar, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const calendarData = {
      calendar_id: calendar.calendar_id || uuidv4(), // Generate a new UUID if missing
      meeting_id: calendar.meeting_id,
      title: calendar.title,
      details: calendar.details,
    };

    try {
      const response = await fetch(BACKEND_BASE_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(calendarData),
      });

      if (response.status === 201) {
        setResponseMessage('Calendar added successfully!');
        onSubmit(calendarData); // Pass the new calendar back to the parent
        setCalendar({ ...calendar, title: '', details: '' }); // Reset form fields
      } else {
        const result = await response.json();
        setResponseMessage(`Failed to add calendar: ${result.error || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Error adding calendar:', error);
      setResponseMessage('Error adding calendar. Please try again.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>Calendar ID:</label>
      <input type="text" name="calendar_id" value={calendar.calendar_id} readOnly />

      <label>Meeting ID:</label>
      <input type="text" name="meeting_id" value={calendar.meeting_id} readOnly />

      <label>Calendar Title:</label>
      <input type="text" name="title" value={calendar.title} onChange={handleChange} required />

      <label>Calendar Details:</label>
      <textarea name="details" value={calendar.details} onChange={handleChange} required></textarea>

      <button type="submit">Add Calendar</button>
      {responseMessage && <p>{responseMessage}</p>}
    </form>
  );
};

export default CalendarForm;
