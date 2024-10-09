import React from 'react';

const MeetingParticipantList = ({ participantList }) => {
    if (!participantList || participantList.length === 0) {
        return <p>No participants to display.</p>;
    }

    return (
        <div>
            <h2>Participant List</h2>
            <ul>
                {participantList.map((participant, index) => (
                    <li key={index}>
                        <strong>{participant.name}</strong><br />
                        {participant.email}<br />
                        {participant.participant_id}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default MeetingParticipantList;
