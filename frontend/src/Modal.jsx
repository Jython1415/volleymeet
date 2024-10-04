import React, { useState } from 'react'
import PropTypes from 'prop-types'

const Modal = ({ isOpen, onClose, title: initialTitle, onSave }) => {
  const [title, setTitle] = useState(initialTitle || 'title');

  const handleSubmit = () => {
    onSave({title});
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="modal">
      <div className="modal-content">
        <h2>{initialTitle ? "Edit Event" : "Add Event"}</h2>
        <input
          type="text"
          value={title}
          onChange={e => setTitle(e.target.value)}
          placeholder="Event Title"
        />
        <button onClick={handleSubmit}>Save</button>
        <button onClick={onClose}>Cancel</button>
      </div>
    </div>
  );
};

Modal.propTypes = {
    isOpen: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
    title: PropTypes.string,
    onSave: PropTypes.func.isRequired,
  };

export default Modal;
