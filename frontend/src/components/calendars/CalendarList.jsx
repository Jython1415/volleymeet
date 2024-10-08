import React from 'react';

const CalendarList = ({ calendars }) => {
    return (
        <table>
            <thead>
                <tr>
                    <th>Calendar Id</th>
                    <th>Title</th>
                    <th>Details</th>
                </tr>
            </thead>
            <tbody>
                {calendars.map((calendar) => (
                    <tr key={calendar.calendar_id}>
                        <td>{calendar.calendar_id}</td>
                        <td>{calendar.title}</td>
                        <td>{calendar.details}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default CalendarList;