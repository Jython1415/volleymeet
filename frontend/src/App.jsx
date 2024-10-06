import React, { useState, useCallback, useMemo } from 'react'
import { Calendar, momentLocalizer, Views } from 'react-big-calendar'
import moment from 'moment'
import { data } from './Data';
import Modal from './Modal';
import './App.css'
import 'react-big-calendar/lib/sass/styles.scss'; 
import 'react-big-calendar/lib/addons/dragAndDrop/styles.scss';


const localizer = momentLocalizer(moment);

const App = () => {

  const [myEvents, setEvents] = useState(data)
  const [isModalOpen, setModalOpen] = useState(false)
  const [currentEvent, setCurrentEvent] = useState(null)
  const [slotDetails, setSlotDetails] = useState({})

  const handleSelectSlot = useCallback(({ start, end }) => {
    setSlotDetails({ start, end });
    setModalOpen(true);
  }, []);

  const handleSelectEvent = useCallback(event => {
    setCurrentEvent(event);
    setModalOpen(true);
  }, [])

  const handleSave = ({title, start, end}) => {
    if (currentEvent) {
      setEvents(prev =>
        prev.map(evt =>
          evt === currentEvent ? { ...evt, title, start, end } : evt
        )
      )
    } else {
      setEvents(prev => [...prev, { title, start, end }])
    }
    setCurrentEvent(null)
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
          events={myEvents}
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
          setSlotDetails({});
        }}
        title={currentEvent ? currentEvent.title : ''} 
        start={currentEvent ? currentEvent.start : new Date()}
        end={currentEvent ? currentEvent.end : new Date()}
        onSave={handleSave}
      />
    </div>
  );
};

export default App