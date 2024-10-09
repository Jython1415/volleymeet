import React from 'react';

const MeetingList = ({ meetings, participants }) => {
    return (
        <table>
            <thead>
                <tr>
                    <th>Meeting Id</th>
                    <th>Title</th>
                    <th>Date Time</th>
                    <th>Location</th>
                    <th>Details</th>
                    <th>Participants</th>
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
                            {participants
                                .filter(participant => participant.meeting_id === meeting.meeting_id)
                                .map(participant => (
                                    <div key={participant.participant_id}>
                                        {participant.name} ({participant.email})
                                    </div>
                                ))}
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default MeetingList;