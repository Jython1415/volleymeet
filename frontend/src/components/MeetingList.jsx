import React from 'react';

const MeetingList = ({ meetings }) => {
    return (
        <table>
            <thead>
                <tr>
                    <th>Title</th>
                    <th>Date and Time</th>
                    <th>Location</th>
                    <th>Participants</th>
                </tr>
            </thead>
            <tbody>
                {meetings.map((meeting) => (
                    <tr key={meeting.id}>
                        <td>{meeting.title}</td>
                        <td>{meeting.dateTime}</td>
                        <td>{meeting.location}</td>
                        <td>{meeting.participantIds.join(', ')}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default MeetingList;