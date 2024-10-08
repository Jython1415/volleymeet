import React, { useState } from 'react';
import CreateMeetingForm from './components/CreateMeetingForm';
import MeetingList from './components/MeetingList';
import ButtonsComponent from './components/ButtonsComponent';
import FindMeetingForm from './components/FindMeetingForm';
import DeleteMeetingForm from './components/DeleteMeetingForm';
import UpdateMeetingForm from './components/UpdateMeetingForm';

const MEETINGS_BACKEND_BASE_URL = "http://localhost:5001/meetings";

function App() {
  const [meetings, setMeetings] = useState([]);
  const [showMeetingForm, setShowMeetingForm] = useState(false);
  const [showMeetingList, setShowMeetingList] = useState(false);
  const [showFindMeetingForm, setShowFindMeetingForm] = useState(false)
  const [showDeleteMeetingForm, setShowDeleteMeetingForm] = useState(false)
  const [showUpdateMeetingForm, setShowUpdateMeetingForm] = useState(false)
  const [responseMessage, setResponseMessage] = useState('');
  const [error, setError] = useState('');


  // Helper function to reset all form visibility states
  const resetFormVisibility = () => {
    setShowMeetingForm(false);
    setShowMeetingList(false);
    setShowFindMeetingForm(false);
    setShowDeleteMeetingForm(false);
    setShowUpdateMeetingForm(false);
    setResponseMessage('');
    setError('');
  };

  const createMeeting = (meeting) => {
    resetFormVisibility();
    setError('');
    setMeetings([...meetings, meeting]);
    setShowMeetingForm(false);
  };

  const handleCreateMeeting = () => {
    resetFormVisibility();
    setShowMeetingForm(true);
  };

  const handleFindMeeting = () => {
    resetFormVisibility();
    setError('');
    setShowFindMeetingForm(true);
  }

  const handleShowDeleteMeeting = () => {
    resetFormVisibility();
    setShowDeleteMeetingForm(true);
  }

  const handleShowUpdateMeeting = () => {
    resetFormVisibility();
    setShowUpdateMeetingForm(true);
  }

  const handleFindMeetingById = async (meetingId) => {
    setError('');

    try {
      const response = await fetch(`${MEETINGS_BACKEND_BASE_URL}/${meetingId}`);
      if (response.status === 200) {
        const meeting = await response.json();
        console.log(meeting); // Handle the found meeting (display it, save it to state, etc.)
        setMeetings([meeting]); // Set the fetched meeting as the only meeting in the list
        setShowMeetingList(true); // Show the meeting list with just this meeting
        setError("");
      } else if (response.status === 404) {
        setError("Meeting not found.");
        setShowMeetingList(false);
      } else {
        setError(`Failed to fetch meeting with status code ${response.status}`);
        setShowMeetingList(false);
      }
    } catch (err) {
      console.error('Error fetching the meeting:', err);
      setError('Error fetching the meeting.');
      setShowMeetingList(false);
    }
  };

  // Function to handle fetching all meetings from the backend
  const handleMeetingDisplay = async () => {
    resetFormVisibility();
    setError('');

    try {
      const response = await fetch(MEETINGS_BACKEND_BASE_URL);

      if (response.status === 200) {
        const data = await response.json();
        console.log(data)
        setMeetings(data); // Set the fetched meetings in the state
        setShowMeetingList(true);
      } else if (response.status === 404) {
        setError("No meetings found.");
        setShowMeetingList(false);
      } else {
        setError(`Failed to fetch meetings with status code ${response.status}`);
        setShowMeetingList(false);
      }
    } catch (err) {
      console.error('Error fetching meetings:', err);
      setError('Error fetching meetings. Please check the backend.');
      setShowMeetingList(false);
    }
  };

  const handleDeleteMeeting = async (meetingId) => {
    setError('');
    setResponseMessage('');

    try {
      const response = await fetch(`${MEETINGS_BACKEND_BASE_URL}/${meetingId}`, {
        method: 'DELETE',
      });

      if (response.status === 204) {
        setMeetings(meetings.filter((meeting) => meeting.meeting_id !== meetingId)); // Remove deleted meeting from state
        setResponseMessage(`Meeting with ID ${meetingId} deleted successfully.`);
      } else if (response.status === 404) {
        setError(`Meeting with ID ${meetingId} not found.`);
      } else {
        setError(`Failed to delete meeting with status code ${response.status}`);
      }
    } catch (err) {
      console.error('Error deleting meeting:', err);
      setError('Error deleting meeting.');
    }
  };


  return (
    <div className="App">
      <ButtonsComponent
        onCreate={handleCreateMeeting}
        onDisplay={handleMeetingDisplay}
        onFind={handleFindMeeting}
        onDelete={handleShowDeleteMeeting}
        onEdit={handleShowUpdateMeeting}
      />
      {showMeetingForm && <CreateMeetingForm onSubmit={createMeeting} />}
      {showMeetingList && <MeetingList meetings={meetings} />}
      {showFindMeetingForm && <FindMeetingForm onFindMeeting={handleFindMeetingById} />}
      {showDeleteMeetingForm && <DeleteMeetingForm onDeleteMeeting={handleDeleteMeeting} />}
      {showUpdateMeetingForm && <UpdateMeetingForm />}
      {responseMessage && <p>{responseMessage}</p>}
      {error && <p>{error}</p>}
    </div>
  );
}

export default App;