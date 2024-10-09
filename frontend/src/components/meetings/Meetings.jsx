import React, { useState } from 'react';
import CreateMeetingForm from './CreateMeetingForm';
import MeetingList from './MeetingList';
import FindMeetingForm from './FindMeetingForm';
import DeleteMeetingForm from './DeleteMeetingForm';
import UpdateMeetingForm from './UpdateMeetingForm';
import LinkParticipantForm from './LinkParticipantForm';
import LinkCalendarForm from './LinkCalendarForm';

const MEETINGS_BACKEND_BASE_URL = "http://localhost:5001/meetings";
const PARTICIPANTS_BACKEND_BASE_URL = "http://localhost:5001/participants";
const ATTACHMENTS_BACKEND_BASE_URL = "http://localhost:5001/attachments";

const Meetings = () => {
    const [meetings, setMeetings] = useState([]);
    const [participants, setParticipants] = useState([]);
    const [attachments, setAttachments] = useState([]);
    const [showCreateMeetingForm, setShowCreateMeetingForm] = useState(false);
    const [showMeetingList, setShowMeetingList] = useState(false);
    const [showFindMeetingForm, setShowFindMeetingForm] = useState(false);
    const [showDeleteMeetingForm, setShowDeleteMeetingForm] = useState(false);
    const [showUpdateMeetingForm, setShowUpdateMeetingForm] = useState(false);
    const [showLinkParticipantForm, setShowLinkParticipantForm] = useState(false);
    const [showLinkCalendarForm, setShowLinkCalendarForm] = useState(false);
    const [responseMessage, setResponseMessage] = useState('');
    const [error, setError] = useState('');

    // Helper function to reset all form visibility states
    const resetFormVisibility = () => {
        setShowCreateMeetingForm(false);
        setShowMeetingList(false);
        setShowFindMeetingForm(false);
        setShowDeleteMeetingForm(false);
        setShowUpdateMeetingForm(false);
        setShowLinkParticipantForm(false);
        setShowLinkCalendarForm(false);
        setResponseMessage('');
        setError('');
    };

    const handleCreateMeeting = () => {
        resetFormVisibility();
        setShowCreateMeetingForm(true);
    };

    const handleFindMeeting = () => {
        resetFormVisibility();
        setShowFindMeetingForm(true);
    };

    const handleShowDeleteMeeting = () => {
        resetFormVisibility();
        setShowDeleteMeetingForm(true);
    };

    const handleShowUpdateMeeting = () => {
        resetFormVisibility();
        setShowUpdateMeetingForm(true);
    };

    const handleShowLinkParticipant = () => {
        resetFormVisibility();
        setShowLinkParticipantForm(true); // Show the link participant form
    };

    const handleShowLinkCalendar = () => {
        resetFormVisibility();
        setShowLinkCalendarForm(true);
    };

    const handleFindMeetingById = async (meetingId) => {
        try {
            const response = await fetch(`${MEETINGS_BACKEND_BASE_URL}/${meetingId}`);
            if (response.status === 200) {
                const meeting = await response.json();
                setMeetings([meeting]);
                setShowMeetingList(true);
                await handleFetchParticipants();
                await handleFetchAttachments();
            } else if (response.status === 404) {
                setError("Meeting not found.");
            } else {
                setError(`Failed to fetch meeting with status code ${response.status}`);
            }
        } catch (err) {
            setError('Error fetching the meeting.');
        }
    };

    const handleMeetingDisplay = async () => {
        resetFormVisibility();
        try {
            const response = await fetch(MEETINGS_BACKEND_BASE_URL);
            if (response.status === 200) {
                const data = await response.json();
                setMeetings(data);
                setShowMeetingList(true);
                await handleFetchParticipants();
                await handleFetchAttachments();
            } else if (response.status === 404) {
                setError("No meetings found.");
            } else {
                setError(`Failed to fetch meetings with status code ${response.status}`);
            }
        } catch (err) {
            setError('Error fetching meetings.');
        }
    };

    const handleDeleteMeeting = async (meetingId) => {
        try {
            const response = await fetch(`${MEETINGS_BACKEND_BASE_URL}/${meetingId}`, {
                method: 'DELETE',
            });
            if (response.status === 204) {
                setMeetings(meetings.filter((meeting) => meeting.meeting_id !== meetingId));
                setResponseMessage(`Meeting with ID ${meetingId} deleted successfully.`);
            } else if (response.status === 404) {
                setError(`Meeting with ID ${meetingId} not found.`);
            } else {
                setError(`Failed to delete meeting with status code ${response.status}`);
            }
        } catch (err) {
            setError('Error deleting meeting.');
        }
    };

    const handleFetchParticipants = async () => {
        try {
            const response = await fetch(PARTICIPANTS_BACKEND_BASE_URL);
            if (response.status === 200) {
                const data = await response.json();
                setParticipants(data);
            } else {
                setError(`Failed to fetch participants with status code ${response.status}`);
            }
        } catch (err) {
            setError('Error fetching participants.');
        }
    };

    const handleFetchAttachments = async () => {
        try {
            const response = await fetch(ATTACHMENTS_BACKEND_BASE_URL);
            if (response.status === 200) {
                const data = await response.json();
                setAttachments(data);
            } else {
                setError(`Failed to fetch participants with status code ${response.status}`);
            }
        } catch (err) {
            setError('Error fetching participants.');
        }
    };

    // Function to link participant to a meeting
    const handleLinkParticipant = async (meetingId, participantId) => {
        try {
            const response = await fetch(`${MEETINGS_BACKEND_BASE_URL}/${meetingId}/participants/${participantId}`, {
                method: 'POST',
            });
            if (response.status === 201) {
                setResponseMessage(`Participant ${participantId} successfully linked to meeting ${meetingId}.`);
            } else {
                setError(`Failed to link participant with status code ${response.status}`);
            }
        } catch (err) {
            setError('Error linking participant to meeting.');
        }
    };

    // Function to link a calendar to a meeting
    const handleLinkCalendar = async (meetingId, calendarId) => {
        try {
            const response = await fetch(`${MEETINGS_BACKEND_BASE_URL}/${meetingId}/calendars/${calendarId}`, {
                method: 'POST',
            });
            if (response.status === 201) {
                setResponseMessage(`Calendar ${calendarId} successfully linked to meeting ${meetingId}.`);
            } else {
                setError(`Failed to link calendar with status code ${response.status}`);
            }
        } catch (err) {
            setError('Error linking calendar to meeting.');
        }
    };

    return (
        <div>
            <button onClick={handleCreateMeeting}>Create Meeting</button>
            <button onClick={handleMeetingDisplay}>Display Meetings</button>
            <button onClick={handleFindMeeting}>Find Meeting</button>
            <button onClick={handleShowDeleteMeeting}>Delete Meeting</button>
            <button onClick={handleShowUpdateMeeting}>Update Meeting</button>
            <button onClick={handleShowLinkParticipant}>Link Participant</button>
            <button onClick={handleShowLinkCalendar}>Link Calendar</button>

            {showCreateMeetingForm && <CreateMeetingForm />}
            {showMeetingList && <MeetingList meetings={meetings} participants={participants} attachments={attachments} />}
            {showFindMeetingForm && <FindMeetingForm onFindMeeting={handleFindMeetingById} />}
            {showDeleteMeetingForm && <DeleteMeetingForm onDeleteMeeting={handleDeleteMeeting} />}
            {showUpdateMeetingForm && <UpdateMeetingForm />}
            {showLinkParticipantForm && <LinkParticipantForm onLinkParticipant={handleLinkParticipant} />}
            {showLinkCalendarForm && <LinkCalendarForm onLinkCalendar={handleLinkCalendar} />}
            {responseMessage && <p>{responseMessage}</p>}
            {error && <p>{error}</p>}
        </div>
    );
};

export default Meetings;
