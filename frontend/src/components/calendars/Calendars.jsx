import React, { useState } from 'react';

const CALENDARS_BACKEND_BASE_URL = "http://localhost:5001/participants";

const Calendars = () => {
    const handleCreateCalendar = () => {
    };

    const handleCalendarDisplay = () => {
    }

    const handleFindCalendar = () => {
    }

    const handleShowDeleteCalendar = () => {
    }

    const handleShowUpdateCalendar = () => {
    }


    return (
        <div>
            <button onClick={handleCreateCalendar}>Create Calendar</button>
            <button onClick={handleCalendarDisplay}>Display Calendars</button>
            <button onClick={handleFindCalendar}>Find Calendar</button>
            <button onClick={handleShowDeleteCalendar}>Delete Calendar</button>
            <button onClick={handleShowUpdateCalendar}>Update Calendar</button>
        </div>
    )
}

export default Calendars;
