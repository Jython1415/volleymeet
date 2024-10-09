import React, { useState } from 'react';
import Meetings from './components/meetings/Meetings';
import Participants from './components/participants/Participants';
import Calendars from './components/calendars/Calendars';
import Attachments from './components/attachments/Attachments';

function App() {
  const [showMeetingsPage, setShowMeetingsPage] = useState(false);
  const [showParticipantsPage, setShowParticipantsPage] = useState(false);
  const [showCalendarsPage, setShowCalendarsPage] = useState(false);
  const [showAttachmentsPage, setShowAttachmentsPage] = useState(false);

  const resetComponentsVisibility = () => {
    setShowMeetingsPage(false);
    setShowParticipantsPage(false);
    setShowCalendarsPage(false);
    setShowAttachmentsPage(false);
  }

  const handleMeetings = () => {
    resetComponentsVisibility();
    setShowMeetingsPage(true);
  }

  const handleParticipants = () => {
    resetComponentsVisibility();
    setShowParticipantsPage(true);
  }

  const handleCalendars = () => {
    resetComponentsVisibility();
    setShowCalendarsPage(true);
  }

  const handleAttachments = () => {
    resetComponentsVisibility();
    setShowAttachmentsPage(true);
  }

  return (
    <div className="App">
      <button onClick={handleMeetings}>Meetings</button>
      <button onClick={handleParticipants}>Participants</button>
      <button onClick={handleCalendars}>Calendars</button>
      <button onClick={handleAttachments}>Attachments</button>

      {/* Blank space between buttons and components */}
      <div style={{ margin: '20px 0' }}></div>

      {showMeetingsPage && <Meetings />}
      {showParticipantsPage && <Participants />}
      {showCalendarsPage && <Calendars />}
      {showAttachmentsPage && <Attachments />}
    </div>
  );
}

export default App;