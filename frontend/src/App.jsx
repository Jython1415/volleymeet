import React, { useState } from 'react';
import CreateMeetingForm from './components/CreateMeetingForm';
import MeetingList from './components/MeetingList';
import ButtonsComponent from './components/ButtonsComponent';

const MEETINGS_BACKEND_BASE_URL = "http://localhost:5001/meetings"; // Your backend URL

function App() {
  const [meetings, setMeetings] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [showList, setShowList] = useState(false);
  const [error, setError] = useState('');

  const createMeeting = (meeting) => {
    setMeetings([...meetings, meeting]);
    setShowForm(false);
  };

  const handleCreate = () => setShowForm(true);

  // Function to handle fetching all meetings from the backend
  const handleDisplay = async () => {
    setShowForm(false); // Hide form when showing list

    try {
      const response = await fetch(MEETINGS_BACKEND_BASE_URL);

      if (response.status === 200) {
        const data = await response.json();
        setMeetings(data); // Set the fetched meetings in the state
        setShowList(true);
      } else if (response.status === 404) {
        setError("No meetings found.");
        setShowList(false);
      } else {
        setError(`Failed to fetch meetings with status code ${response.status}`);
        setShowList(false);
      }
    } catch (err) {
      console.error('Error fetching meetings:', err);
      setError('Error fetching meetings. Please check the backend.');
      setShowList(false);
    }
  };

  return (
    <div className="App">
      <ButtonsComponent
        onCreate={handleCreate}
        onDisplay={handleDisplay}
        onFind={() => { }}
        onDelete={() => { }}
        onEdit={() => { }}
      />
      {showForm && <CreateMeetingForm onSubmit={createMeeting} />}
      {showList && <MeetingList meetings={meetings} />}
      {error && <p>{error}</p>}
    </div>
  );
}

export default App;