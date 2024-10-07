import React, { useState } from 'react';
import ParticipantForm from './ParticipantForm';
import CalendarForm from './CalendarForm';

const CreateMeetingForm = ({ onSubmit }) => {
  const [meeting, setMeeting] = useState({
    id: '',
    title: '',
    dateTime: '',
    location: '',
    details: '',
    calendarIds: [],
    participantIds: [],
    attachmentIds: [],
  });

  const [participants, setParticipants] = useState([]);
  const [calendars, setCalendars] = useState([]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setMeeting({ ...meeting, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!meeting.id) {
      meeting.id = generateUUID(); // If UUID is not provided, generate one
    }
    onSubmit(meeting);
  };

  const generateUUID = () => {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
      const r = (Math.random() * 16) | 0;
      const v = c === 'x' ? r : (r & 0x3) | 0x8;
      return v.toString(16);
    });
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
      <form onSubmit={handleSubmit}>
        <label>Meeting ID:</label>
        <input type="text" name="id" value={meeting.id} onChange={handleChange} readOnly />

        <label>Meeting Title:</label>
        <input type="text" name="title" value={meeting.title} onChange={handleChange} maxLength="2000" required />

        <label>Date and Time:</label>
        <input type="text" name="dateTime" value={meeting.dateTime} onChange={handleChange} placeholder="YYYY-MM-DD HH:MM AM/PM" required />

        <label>Location:</label>
        <input type="text" name="location" value={meeting.location} onChange={handleChange} maxLength="2000" required />

        <label>Details:</label>
        <textarea name="details" value={meeting.details} onChange={handleChange} maxLength="10000" required></textarea>

        <button type="submit">Create Meeting</button>
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
