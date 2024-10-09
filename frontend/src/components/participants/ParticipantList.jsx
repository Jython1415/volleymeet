import React from 'react';

const ParticipantList = ({ participants }) => {
    return (
        <table>
            <thead>
                <tr>
                    <th>Participant Id</th>
                    <th>Name</th>
                    <th>Email</th>
                </tr>
            </thead>
            <tbody>
                {participants.map((participant) => (
                    <tr key={participant.participant_id} style={{ marginBottom: '20px' }}>
                        <td>{participant.participant_id}</td>
                        <td>{participant.name}</td>
                        <td>{participant.email}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default ParticipantList;