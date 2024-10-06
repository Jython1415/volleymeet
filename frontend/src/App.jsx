import React, { useState } from 'react';
import CreateMeetingForm from './components/CreateMeetingForm';
import MeetingList from './components/MeetingList';
import ButtonsComponent from './components/ButtonsComponent';

const MEETINGS_BACKEND_BASE_URL = "http://localhost:5001/meetings"; // Your backend URL

function App() {
  const [meetings, setMeetings] = useState([]);
  const [showMeetingForm, setShowMeetingForm] = useState(false);
  const [showMeetingList, setShowMeetingList] = useState(false);
  const [error, setError] = useState('');

  const createMeeting = (meeting) => {
    setMeetings([...meetings, meeting]);
    setShowMeetingForm(false);
  };

  const handleCreateMeeting = () => setShowMeetingForm(true);

  // Function to handle fetching all meetings from the backend
  const handleMeetingDisplay = async () => {
    setShowMeetingForm(false); // Hide form when showing list

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

  return (
    <div className="App">
      <ButtonsComponent
        onCreate={handleCreateMeeting}
        onDisplay={handleMeetingDisplay}
        onFind={() => { }}
        onDelete={() => { }}
        onEdit={() => { }}
      />
      {showMeetingForm && <CreateMeetingForm onSubmit={createMeeting} />}
      {showMeetingList && <MeetingList meetings={meetings} />}
      {error && <p>{error}</p>}
    </div>
  );
}

export default App;