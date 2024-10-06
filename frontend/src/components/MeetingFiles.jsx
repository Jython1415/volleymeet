import React, { useState } from 'react';

const MeetingFiles = ({ files, onAddFile, onRemoveFile }) => {
  const [fileUrl, setFileUrl] = useState('');

  const handleAddFile = (e) => {
    e.preventDefault();
    if (fileUrl) {
      onAddFile(fileUrl);
      setFileUrl(''); // Clear the input field after adding the file
    }
  };

  const handleRemoveFile = (fileUrlToRemove) => {
    onRemoveFile(fileUrlToRemove);
  };

  return (
    <div>
      <h3>Meeting Attachments</h3>
      <form onSubmit={handleAddFile}>
        <label htmlFor="fileUrl">Attachment URL:</label>
        <input
          type="url"
          id="fileUrl"
          value={fileUrl}
          onChange={(e) => setFileUrl(e.target.value)}
          required
        />
        <button type="submit">Add Attachment</button>
      </form>

      {files.length > 0 && (
        <ul>
          {files.map((file, index) => (
            <li key={index}>
              <a href={file} target="_blank" rel="noopener noreferrer">
                {file}
              </a>
              <button onClick={() => handleRemoveFile(file)}>Remove</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default MeetingFiles;
