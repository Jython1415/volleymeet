import React, { useState } from 'react'
import PropTypes from 'prop-types'

const Modal = ({ isOpen, onClose, title: initialTitle, start: initialStart, end: initialEnd, onSave }) => {
  const [title, setTitle] = useState(initialTitle || '');
  const [start, setStart] = useState(initialStart || new Date())
  const [end, setEnd] = useState(initialEnd || new Date())

  const handleTimeChange = (timeString, setter) => {
    const [ hours, minutes] = timeString.split(':')
    const newDate = new Date(start)
    newDate.setHours(hours, minutes)
    setter(newDate)
  }

  const handleSubmit = () => {
    onSave({title, start, end});
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="modal">
      <div className="modal-content">
        <h2>{initialTitle ? "Edit Event" : "Add Event"}</h2>
        <div>
            <label>
                Title: 
                <input
                    type="text"
                    value={title}
                    onChange={e => setTitle(e.target.value)}
                    placeholder="Event Title"
                />
            </label>
        </div>
        <div>
            <label>
                Start Time:
                <input
                    type="time"
                    value={`${start.getHours().toString().padStart(2, '0')}:${start.getMinutes().toString().padStart(2, '0')}`}
                    onChange={e => handleTimeChange(e.target.value, setStart)}
                />
            </label>
        </div>
        <div>
            <label>
                End Time:
                <input
                    type="time"
                    value={`${end.getHours().toString().padStart(2, '0')}:${end.getMinutes().toString().padStart(2, '0')}`}
                    onChange={e => handleTimeChange(e.target.value, setEnd)}
                />
            </label>
        </div>
        <div>
            <button onClick={handleSubmit}>Save</button>
            <button onClick={onClose}>Cancel</button>
        </div>
      </div>
    </div>
  );
};

Modal.propTypes = {
    isOpen: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
    title: PropTypes.string,
    start: PropTypes.instanceOf(Date),
    end: PropTypes.instanceOf(Date),
    onSave: PropTypes.func.isRequired,
};

export default Modal;
