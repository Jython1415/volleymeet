import { useState } from 'react'
import Calendar from'react-calendar'
import TimePicker from 'react-time-picker'
import './App.css'
import './Calendar.css'
import 'react-time-picker/dist/TimePicker.css'

const App = () => {
  const [calValue, setCalValue] = useState(new Date());
  const [timeValue, onChangeTime] = useState('10:00');

  return (
    <div>
      <h1>Select Meeting Date</h1>
      <div className='calendar-container'>
        <Calendar onChange={setCalValue} value={calValue} />
      </div>
      <h2>Selected date: {calValue.toDateString()}</h2>
      <div className='time-picker-container'>
        <TimePicker onChange={onChangeTime} value={timeValue}/>
      </div>
    </div>
  );
};

export default App
