import { useState } from 'react'
/*import Calendar from'react-calendar'*/
import { Calendar, momentLocalizer } from 'react-big-calendar'
import moment from 'moment'
/*import './App.css'
import './Calendar.css'
import 'react-big-calendar/lib/css/react-big-calendar.css'*/
import 'react-big-calendar/lib/sass/styles.scss'; 
import 'react-big-calendar/lib/addons/dragAndDrop/styles.scss';

const myEventsList = [
  {
    title: 'Meeting',
    start: new Date(2024, 9, 7, 10, 0), // Example event start date/time
    end: new Date(2024, 9, 7, 12, 0),   // Example event end date/time
  },
  {
    title: 'Conference',
    start: new Date(2024, 9, 8, 11, 0),
    end: new Date(2024, 9, 8, 14, 0),
  },
];

const localizer = momentLocalizer(moment);

const App = () => {

  return (
    <div>
      <h1>Select Meeting Date</h1>
      <div className='calendar-container'>
        <Calendar
          localizer={localizer}
          events={myEventsList}
          startAccessor="start"
          endAccessor="end"
          style={{ height: 500 }}
        />
      </div>
    </div>
  );
};

export default App