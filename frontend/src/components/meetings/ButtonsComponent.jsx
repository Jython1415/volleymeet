import React from 'react';

const ButtonsComponent = ({ onCreate, onDisplay, onFind, onDelete, onEdit }) => {
    return (
        <div>
            <button onClick={onCreate}>Create Meeting</button>
            <button onClick={onDisplay}>Display All Meetings</button>
            <button onClick={onFind}>Find Meeting</button>
            <button onClick={onDelete}>Delete Meeting</button>
            <button onClick={onEdit}>Edit Meeting</button>
        </div>
    );
};

export default ButtonsComponent;