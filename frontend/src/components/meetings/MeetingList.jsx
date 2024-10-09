import React from 'react';

const MeetingList = ({ meetings, participants, attachments }) => {
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
                    <th>Attachments</th>
                </tr>
            </thead>
            <tbody>
                {meetings.map((meeting) => (
                    <tr key={meeting.meeting_id} style={{ marginBottom: '20px' }}>
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
                        <td>
                            {attachments
                                .filter(attachments => attachments.meeting_id === meeting.meeting_id)
                                .map(attachment => (
                                    <div key={attachment.attachment_id}>
                                        {attachment.attachment_id} ({attachment.attachment_url})
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