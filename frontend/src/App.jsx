import React, { useState } from 'react';
import CreateMeetingForm from './components/CreateMeetingForm';
import MeetingList from './components/MeetingList';
import ButtonsComponent from './components/ButtonsComponent';
import ParticipantForm from './components/ParticipantForm';
import FindMeetingForm from './components/FindMeetingForm';
import DeleteMeetingForm from './components/DeleteMeetingForm';

const MEETINGS_BACKEND_BASE_URL = "http://localhost:5001/meetings";

function App() {
  const [meetings, setMeetings] = useState([]);
  const [selectedMeetingId, setSelectedMeetingId] = useState(null)
  const [participants, setParticipants] = useState([])
  const { showParticipantForm, setShowParticipantForm } = useState(false)
  const [attachments, setAttachments] = useState([])
  const [showMeetingForm, setShowMeetingForm] = useState(false);
  const [showMeetingList, setShowMeetingList] = useState(false);
  const [showAttachmentForm, setAttachmentForm] = useState(false)
  const [showFindMeetingForm, setShowFindMeetingForm] = useState(false)
  const [showDeleteMeetingForm, setShowDeleteMeetingForm] = useState(false)
  const [responseMessage, setResponseMessage] = useState('');
  const [error, setError] = useState('');

  const createMeeting = (meeting) => {
    setError('');
    setMeetings([...meetings, meeting]);
    setShowMeetingForm(false);
  };

  const handleCreateMeeting = () => {
    setShowMeetingForm(prevState => !prevState);
  };

  const handleFindMeeting = () => {
    setError('');
    setShowMeetingForm(false);
    setShowMeetingList(false);
    setShowFindMeetingForm(prevState => !prevState);
  }

  const handleShowDeleteMeeting = () => {
    setShowDeleteMeetingForm(prevState => !prevState);
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
    setError('');
    setShowMeetingForm(false); // Hide meeting form when showing list
    setShowFindMeetingForm(false);

    try {
      const response = await fetch(MEETINGS_BACKEND_BASE_URL);

      if (response.status === 200) {
        const data = await response.json();
        console.log(data)
        setMeetings(data); // Set the fetched meetings in the state
        setShowMeetingList(prevState => !prevState);
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

  const handleAddParticipant = (participant) => {
    setParticipants([...participants, participant])
  }

  const handleShowParticipants = async (meeting_id) => {
    try {
      const response = await fetch('${MEETINGS_BACKEND_BASE_URL}/${meeting_id') // is this the rightway to reference this?
      if (response.status === 200) {
        const data = await response.json()
        setParticipants(data)
        setSelectedMeetingId(meeting_id)
        setShowParticipantForm(true)
      } else {
        setError('Failed to fetch participants with status code ${response.status}')
      }
    } catch (error) {
      console.error('Error fetching participants: ', error)
      setError('Error fetching participants')
    }
  }

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
        onFind={handleFindMeeting}
        onDelete={handleShowDeleteMeeting}
        onEdit={() => { }}
      />
      {showMeetingForm && <CreateMeetingForm onSubmit={createMeeting} />}
      {showMeetingList && <MeetingList meetings={meetings} onAddAttachment={handleShowAttachments} onShowParticpants={handleShowParticipants} />}
      {showAttachmentForm && <MeetingFiles files={attachments} onAddFile={handleAddAttachment} onRemoveFile={handleRemoveAttachment} />}
      {showParticipantForm && (
        <>
          <ParticipantForm meetingId={selectedMeetingId} onSubmit={handleAddParticipant} />
          <ul>
            {participants.map((participant) => (
              <li key={handleAddParticipant.participant_id}>{participant.name} ({participant.email}) </li>
            ))}
          </ul>
        </>
      )}
      {showFindMeetingForm && <FindMeetingForm onFindMeeting={handleFindMeetingById} />}
      {showDeleteMeetingForm && <DeleteMeetingForm onDeleteMeeting={handleDeleteMeeting} />}
      {responseMessage && <p>{responseMessage}</p>}
      {error && <p>{error}</p>}
    </div>
  );
}

export default App;