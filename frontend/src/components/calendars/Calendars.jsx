import React, { useState } from 'react';
import CalendarList from './CalendarList';
import CreateCalendarForm from './CreateCalendarForm';
import FindCalendarForm from './FindCalendarForm';
import DeleteCalendarForm from './DeleteCalendarForm';
import UpdateCalendarForm from './UpdateCalendarForm';

const CALENDARS_BACKEND_BASE_URL = "http://localhost:5001/calendars";

const Calendars = () => {
    const [calendars, setCalendars] = useState([]);
    const [showCreateCalendarForm, setShowCreateCalendarForm] = useState(false);
    const [showCalendarList, setShowCalendarList] = useState(false);
    const [showFindCalendarForm, setShowFindCalendarForm] = useState(false);
    const [showDeleteCalendarForm, setShowDeleteCalendarForm] = useState(false);
    const [showUpdateCalendarForm, setShowUpdateCalendarForm] = useState(false);
    const [responseMessage, setResponseMessage] = useState('');
    const [error, setError] = useState('');


    // Helper function to reset all form visibility states
    const resetFormVisibility = () => {
        setShowCreateCalendarForm(false);
        setShowCalendarList(false);
        setShowFindCalendarForm(false);
        setShowDeleteCalendarForm(false);
        setShowUpdateCalendarForm(false);
        setResponseMessage('');
        setError('');

    }

    const handleCreateCalendar = () => {
        resetFormVisibility();
        setShowCreateCalendarForm(true);
    };

    const handleCalendarDisplay = async () => {
        resetFormVisibility();
        try {
            const response = await fetch(CALENDARS_BACKEND_BASE_URL);
            if (response.status === 200) {
                const data = await response.json();
                setCalendars(data);
                setShowCalendarList(true);
            } else if (response.status === 404) {
                setError("No calendars found.");
            } else {
                setError(`Failed to fetch calendars with status code ${response.status}`);
            }
        } catch (err) {
            setError('Error fetching calendars.');
        }
    };

    const handleFindCalendar = () => {
        resetFormVisibility();
        setShowFindCalendarForm(true);
    }

    const handleShowDeleteCalendar = () => {
        resetFormVisibility();
        setShowDeleteCalendarForm(true);
    }

    const handleShowUpdateCalendar = () => {
        resetFormVisibility();
        setShowUpdateCalendarForm(true);
    }

    const handleDeleteCalendar = async (calendarId) => {
        try {
            const response = await fetch(`${CALENDARS_BACKEND_BASE_URL}/${calendarId}`, {
                method: 'DELETE',
            });
            if (response.status === 204) {
                setCalendars(calendars.filter((calendar) => calendar.calendar_id !== calendarId));
                setResponseMessage(`Calendar with ID ${calendarId} deleted successfully.`);
            } else if (response.status === 404) {
                setError(`Calendar with ID ${calendarId} not found.`);
            } else {
                setError(`Failed to delete calendar with status code ${response.status}`);
            }
        } catch (err) {
            setError('Error deleting calendar.');
        }
    };

    const handleFindCalendarById = async (calendarId) => {
        try {
            const response = await fetch(`${CALENDARS_BACKEND_BASE_URL}/${calendarId}`);
            if (response.status === 200) {
                const calendar = await response.json();
                setCalendars([calendar]);
                setShowCalendarList(true);
            } else if (response.status === 404) {
                setError("Calendar not found.");
            } else {
                setError(`Failed to fetch calendar with status code ${response.status}`);
            }
        } catch (err) {
            setError('Error fetching the calendar.');
        }
    };


    return (
        <div>
            <button onClick={handleCreateCalendar}>Create Calendar</button>
            <button onClick={handleCalendarDisplay}>Display Calendars</button>
            <button onClick={handleFindCalendar}>Find Calendar</button>
            <button onClick={handleShowDeleteCalendar}>Delete Calendar</button>
            <button onClick={handleShowUpdateCalendar}>Update Calendar</button>

            {showCreateCalendarForm && <CreateCalendarForm />}
            {showCalendarList && <CalendarList calendars={calendars} />}
            {showFindCalendarForm && <FindCalendarForm onFindCalendar={handleFindCalendarById} />}
            {showDeleteCalendarForm && <DeleteCalendarForm onDeleteCalendar={handleDeleteCalendar} />}
            {showUpdateCalendarForm && <UpdateCalendarForm />}

            {responseMessage && <p>{responseMessage}</p>}
            {error && <p>{error}</p>}
        </div>
    )
}

export default Calendars;
