import React, { useState } from 'react';
import CreateMeetingForm from './components/CreateMeetingForm';
import MeetingList from './components/MeetingList';
import MeetingFiles from './components/MeetingFiles';
import ButtonsComponent from './components/ButtonsComponent';

const MEETINGS_BACKEND_BASE_URL = "http://localhost:5001/meetings"; // Your backend URL

function App() {
  const [meetings, setMeetings] = useState([]);
  const [selectedMeetingId, setSelectedMeetingId] = useState(null)
  const [attachments, setAttachments] = useState([])
  const [showMeetingForm, setShowMeetingForm] = useState(false);
  const [showMeetingList, setShowMeetingList] = useState(false);
  const [showAttachmentForm, setAttachmentForm] = useState(false)
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

  const handleAddAttachment = async (fileUrl) => {
    if (!selectedMeetingId) return

    const newAttachment = {
      meeting_id: selectedMeetingId,
      file_url: fileUrl
    }

    try {
      const response = await fetch(MEETINGS_BACKEND_BASE_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newAttachment)
      });

      if (response.status === 201) {
        setAttachments([...attachments, fileUrl]); // Add the new attachment to state
      } else {
        setError(`Failed to add attachment with status code ${response.status}`);
      }
    } catch (err) {
      console.error('Error adding attachment:', err);
      setError('Error adding attachment.');
    }
  }

  const handleRemoveAttachment = async (fileUrlToRemove) => {
    try {
      const response = await fetch(`${MEETINGS_BACKEND_BASE_URL}/${selectedMeetingId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ file_url: fileUrlToRemove })
      })

      if (response.status === 200) {
        setAttachments(attachments.filter(file => file !== fileUrlToRemove))
      } else {
        setError(`Failed to remove attachment with status code ${response.status}`)
      }
    } catch (err) {
      console.error('Error removing attachment:', err);
      setError('Error removing attachment.');
    }
  };

  const handleShowAttachments = async (meetingId) => {
    try {
      const response = await fetch(`${ATTACHMENTS_BACKEND_BASE_URL}/${meetingId}`);
      if (response.status === 200) {
        const data = await response.json();
        setAttachments(data); // Set the fetched attachments in the state
        setSelectedMeetingId(meetingId);
        setShowAttachmentForm(true);
      } else {
        setError(`Failed to fetch attachments with status code ${response.status}`);
      }
    } catch (err) {
      console.error('Error fetching attachments:', err);
      setError('Error fetching attachments.');
    }
  }

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
      {showMeetingList && <MeetingList meetings={meetings} onAddAttachment={handleShowAttachments} />}
      {showAttachmentForm && <MeetingFiles files={attachments} onAddFile={handleAddAttachment} onRemoveFile={handleRemoveAttachment} />}
      {error && <p>{error}</p>}
    </div>
  );
}

export default App;