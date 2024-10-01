import { useState } from 'react'
import Calendar from'react-calendar'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import './Calendar.css'

const App = () => {
  const [value, setValue] = useState(new Date());

  return (
    <div>
      <h1>Select Meeting Date</h1>
      <Calendar onChange={setValue} value={value} />
      <h2>Selected date: {value.toDateString()}</h2>
    </div>
  );
};

export default App
