import React from 'react';
// import PropTypes from 'prop-types';

const CalendarMeetingList = ({ meetings }) => {
    return (
        <div>
            <h2>Meeting List</h2>
            <ul>
                {meetings.map((meeting, index) => (
                    <li key={index}>
                        <strong>{meeting.title}</strong><br />
                        {meeting.date} at {meeting.time}<br />
                        {meeting.location}<br />
                        {meeting.meeting_id}
                    </li>
                ))}
            </ul>
        </div>
    );
};

// CalendarMeetingList.propTypes = {
//     meetings: PropTypes.arrayOf(
//         PropTypes.shape({
//             meeting_id: PropTypes.number.isRequired,
//             title: PropTypes.string.isRequired,
//             date: PropTypes.string.isRequired,
//             time: PropTypes.string.isRequired,
//             location: PropTypes.string.isRequired,
//         })
//     ).isRequired,
// };

export default CalendarMeetingList;