import React, { useState } from 'react';
import CreateMeetingForm from './components/CreateMeetingForm';
import MeetingList from './components/MeetingList';
import ButtonsComponent from './components/ButtonsComponent';

function App() {
  const [meetings, setMeetings] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [showList, setShowList] = useState(false);

  const createMeeting = (meeting) => {
    setMeetings([...meetings, meeting]);
    setShowForm(false);
  };

  const handleCreate = () => setShowForm(true);
  const handleDisplay = () => setShowList(true);

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
    </div>
  );
}

export default App;