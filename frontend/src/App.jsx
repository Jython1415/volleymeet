import React, { useState, useCallback, useMemo } from 'react'
import { Calendar, momentLocalizer, Views } from 'react-big-calendar'
import moment from 'moment'
import 'react-big-calendar/lib/sass/styles.scss'; 
import 'react-big-calendar/lib/addons/dragAndDrop/styles.scss';
import { data } from './Data';

const localizer = momentLocalizer(moment);

const App = () => {

  const [myEvents, setEvents] = useState(data)

  const handleSelectSlot = useCallback(({ start, end }) => {
    const title = window.prompt('New Event name')
    if (title) {
      setEvents(prev => [...prev, { start, end, title }])
    }
  })

  const handleSelectEvent = useCallback(event => {
    window.alert(event.title, start, end)
  })

  const { defaultDate, scrollToTime } = useMemo(
    () => ({
      defaultDate: new Date(),
      scrollToTime: new Date(1970, 1, 1, 6),
    }),
    []
  )

  return (
    <div>
      <h1>Select Meeting Date</h1>
      <div className='calendar-container'>
        <Calendar
          selectable
          localizer={localizer}
          events={myEvents}
          startAccessor="start"
          endAccessor="end"
          style={{ height: 500 }}
          onSelectEvent={handleSelectEvent}
          onSelectSlot={handleSelectSlot}
          scrollToTime={scrollToTime}
        />
      </div>
    </div>
  );
};

export default App