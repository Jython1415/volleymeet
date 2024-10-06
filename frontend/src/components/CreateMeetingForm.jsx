import React, { useState } from 'react';
import MeetingFiles from './MeetingFiles';

const CreateMeetingForm = ({ onSubmit }) => {
  const [meeting, setMeeting] = useState({
    id: '',
    title: '',
    dateTime: '',
    location: '',
    details: '',
    calendarIds: [],
    participantIds: [],
    attachmentIds: [], // This will hold the file URLs
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setMeeting({ ...meeting, [name]: value });
  };

  const handleAddFile = (fileUrl) => {
    setMeeting({ ...meeting, attachmentIds: [...meeting.attachmentIds, fileUrl] });
  };

  const handleRemoveFile = (fileUrl) => {
    setMeeting({
      ...meeting,
      attachmentIds: meeting.attachmentIds.filter((url) => url !== fileUrl),
    });
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

  return (
    <form onSubmit={handleSubmit}>
      <label>Meeting ID:</label>
      <input type="text" name="id" value={meeting.id} onChange={handleChange} />

      <label>Meeting Title:</label>
      <input type="text" name="title" value={meeting.title} onChange={handleChange} maxLength="2000" />

      <label>Date and Time:</label>
      <input type="text" name="dateTime" value={meeting.dateTime} onChange={handleChange} placeholder="YYYY-MM-DD HH:MM AM/PM" />

      <label>Location:</label>
      <input type="text" name="location" value={meeting.location} onChange={handleChange} maxLength="2000" />

      <label>Details:</label>
      <textarea name="details" value={meeting.details} onChange={handleChange} maxLength="10000"></textarea>

      <label>Calendar IDs (comma-separated):</label>
      <input type="text" name="calendarIds" value={meeting.calendarIds} onChange={handleChange} />

      <label>Participant IDs (comma-separated):</label>
      <input type="text" name="participantIds" value={meeting.participantIds} onChange={handleChange} />

      {/* Attachments */}
      <MeetingFiles files={meeting.attachmentIds} onAddFile={handleAddFile} onRemoveFile={handleRemoveFile} />

      <button type="submit">Submit</button>
    </form>
  );
};

export default CreateMeetingForm;
