import React, { useState, useCallback, useMemo, useEffect } from 'react'
import { Calendar, momentLocalizer, Views } from 'react-big-calendar'
import moment from 'moment'
import { data } from './Data'
import Modal from './Modal'
import { fetchEvents, addEvent, updateEvent, deleteEvent } from './crudService'
import './App.css'
import 'react-big-calendar/lib/sass/styles.scss'
import 'react-big-calendar/lib/addons/dragAndDrop/styles.scss'


const localizer = momentLocalizer(moment);

const App = () => {

  const [myEvents, setEvents] = useState(data)
  const [isModalOpen, setModalOpen] = useState(false)
  const [currentEvent, setCurrentEvent] = useState(null)
  const [slotDetails, setSlotDetails] = useState({ start:null, end:null })

  // fetches events from the persistence layer
  useEffect(() => {
    fetchEvents().then(response => setEvents(response.data));
  }, []);

  const handleSelectSlot = useCallback(({ start, end }) => {
    setSlotDetails({ start, end })
    setCurrentEvent(null)
    setModalOpen(true)
  }, []);

  const handleSelectEvent = useCallback(event => {
    setCurrentEvent(event);
    setSlotDetails({ start: event.start, end: event.end})
    setModalOpen(true);
  }, [])

  const handleSave = ({title, start, end}) => {
    if (currentEvent) {
      updateEvent(currentEvent.id, newEvent).then(() => {
        setEvents(prev => prev.map(event => (event.id === currentEvent.id ? newEvent : event)))
      })
    } else {
      addEvent(newEvent).then(response => {
        setEvents(prev => [...prev, response.data]);
      })
    }
    setModalOpen(false)
    setCurrentEvent(null)
    setSlotDetails({ start:null, end:null })
  }

  const { defaultDate, scrollToTime } = useMemo(
    () => ({
      defaultDate: new Date(),
      scrollToTime: new Date(1970, 1, 1, 6),
    }),
    []
  )

  return (
    <div>
      <h1>Meeting Calendar</h1>
      <div className='calendar-container'>
        <Calendar
          selectable
          localizer={localizer}
          events={myEvents} /* this is where we're going to import calendar events*/
          startAccessor="start"
          endAccessor="end"
          style={{ height: 500 }}
          onSelectEvent={handleSelectEvent}
          onSelectSlot={handleSelectSlot}
          scrollToTime={scrollToTime}
        />
      </div>
      <Modal
        isOpen={isModalOpen}
        onClose={() => {
          setModalOpen(false);
          setCurrentEvent(null);
          setSlotDetails({ start:null, end:null });
        }}
        title={currentEvent ? currentEvent.title : ''} 
        start={slotDetails.start || new Date()}
        end={slotDetails.end || new Date()}
        onSave={handleSave}
      />
    </div>
  );
};

export default App