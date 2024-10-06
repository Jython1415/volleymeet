import React from 'react';

const MeetingList = ({ meetings }) => {
    return (
        <table>
            <thead>
                <tr>
                    <th>Meeting Id</th>
                    <th>Title</th>
                    <th>Date and Time</th>
                    <th>Location</th>
                    <th>Details</th>
                </tr>
            </thead>
            <tbody>
                {meetings.map((meeting) => (
                    <tr key={meeting.meeting_id}>
                        <td>{meeting.title}</td>
                        <td>{meeting.date_time}</td>
                        <td>{meeting.location}</td>
                        <td>{meeting.details}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default MeetingList;