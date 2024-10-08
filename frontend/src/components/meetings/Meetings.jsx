
import React, { useState } from 'react';
import CreateMeetingForm from './CreateMeetingForm';
import MeetingList from './MeetingList';
import FindMeetingForm from './FindMeetingForm';
import DeleteMeetingForm from './DeleteMeetingForm';
import UpdateMeetingForm from './UpdateMeetingForm';

const MEETINGS_BACKEND_BASE_URL = "http://localhost:5001/meetings";

const Meetings = () => {
    const [meetings, setMeetings] = useState([]);
    const [showCreateMeetingForm, setShowCreateMeetingForm] = useState(false);
    const [showMeetingList, setShowMeetingList] = useState(false);
    const [showFindMeetingForm, setShowFindMeetingForm] = useState(false);
    const [showDeleteMeetingForm, setShowDeleteMeetingForm] = useState(false);
    const [showUpdateMeetingForm, setShowUpdateMeetingForm] = useState(false);
    const [responseMessage, setResponseMessage] = useState('');
    const [error, setError] = useState('');


    // Helper function to reset all form visibility states
    const resetFormVisibility = () => {
        setShowCreateMeetingForm(false);
        setShowMeetingList(false);
        setShowFindMeetingForm(false);
        setShowDeleteMeetingForm(false);
        setShowUpdateMeetingForm(false);
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

    const handleFindMeetingById = async (meetingId) => {
        try {
            const response = await fetch(`${MEETINGS_BACKEND_BASE_URL}/${meetingId}`);
            if (response.status === 200) {
                const meeting = await response.json();
                setMeetings([meeting]);
                setShowMeetingList(true);
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

    return (
        <div>
            <button onClick={handleCreateMeeting}>Create Meeting</button>
            <button onClick={handleMeetingDisplay}>Display Meetings</button>
            <button onClick={handleFindMeeting}>Find Meeting</button>
            <button onClick={handleShowDeleteMeeting}>Delete Meeting</button>
            <button onClick={handleShowUpdateMeeting}>Update Meeting</button>

            {showCreateMeetingForm && <CreateMeetingForm />}
            {showMeetingList && <MeetingList meetings={meetings} />}
            {showFindMeetingForm && <FindMeetingForm onFindMeeting={handleFindMeetingById} />}
            {showDeleteMeetingForm && <DeleteMeetingForm onDeleteMeeting={handleDeleteMeeting} />}
            {showUpdateMeetingForm && <UpdateMeetingForm />}
            {responseMessage && <p>{responseMessage}</p>}
            {error && <p>{error}</p>}
        </div>
    );
};

export default Meetings;
