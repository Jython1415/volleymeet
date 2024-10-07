import React from 'react';

const MeetingList = ({ meetings, onAddAttachment }) => {
    return (
        <table>
            <thead>
                <tr>
                    <th>Meeting Id</th>
                    <th>Title</th>
                    <th>Date and Time</th>
                    <th>Location</th>
                    <th>Details</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {meetings.map((meeting) => (
                    <tr key={meeting.meeting_id}>
                        <td>{meeting.meeting_id}</td>
                        <td>{meeting.title}</td>
                        <td>{meeting.date_time}</td>
                        <td>{meeting.location}</td>
                        <td>{meeting.details}</td>
                        <td>
                            <button onClick={() => onAddAttachment(meeting.meeting_id)}>View/Add Attachments</button>
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default MeetingList;