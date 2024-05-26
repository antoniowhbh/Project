import React, { useState, useRef, useEffect } from 'react';
import './ExamPal.css';

const ExamPal = () => {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState('');
  const [pdfPath, setPdfPath] = useState('');
  const [message, setMessage] = useState('');
  const [chatResponses, setChatResponses] = useState([]);
  const messageInputRef = useRef(null);
  const fileInputRef = useRef(null);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatResponses]);

  const handleFileSelect = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setFileName(selectedFile.name);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file first.');
      return;
    }
    const formData = new FormData();
    formData.append('file', file);
  
    try {
      const response = await fetch('http://localhost:5000/pdfchat/upload', {
        method: 'POST',
        body: formData,
        credentials: 'include'  // Include cookies with the request
      });
      const data = await response.json();
      if (response.ok) {
        setPdfPath(data.path);
        setMessage('');
        messageInputRef.current.focus();
      } else {
        alert('Upload failed: ' + data.error);
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error uploading file.');
    }
  };
  

  const sendMessage = async () => {
    if (!message || !pdfPath) {
      alert("Please upload a file and enter a message before sending.");
      return;
    }
    appendMessage('You', message);
    const payload = { pdf_path: pdfPath, message };
  
    try {
      const response = await fetch('http://localhost:5000/pdfchat/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        credentials: 'include'  // Include cookies with the request
      });
      const data = await response.json();
      if (!response.ok) throw new Error(`HTTP error, status = ${response.status}`);
      appendMessage('Helper', data.response);
      setMessage('');
    } catch (error) {
      console.error('Error:', error);
    }
  };
  

  const appendMessage = (sender, text) => {
    setChatResponses(prevResponses => [...prevResponses, { sender, text }]);
  };

  return (
    <div className="chatbot-container">
      <div className="chat-section">
        {chatResponses.length === 0 && (
          <div className="welcome-message">
            <h1>How can I help you today?</h1>
          </div>
        )}
        <div id="chatResponses" className="chat-responses">
          {chatResponses.map((response, index) => (
            <div key={index} className={`chat-message ${response.sender === 'You' ? 'user-message' : 'bot-message'}`}>
              {response.text}
            </div>
          ))}
          <div ref={chatEndRef}></div>
        </div>
      </div>
      <div className="chat-input-section">
        <form onSubmit={e => { e.preventDefault(); sendMessage(); }}>
          <input
            type="file"
            id="file-upload"
            style={{ display: 'none' }}
            onChange={handleFileSelect}
            ref={fileInputRef}
          />
          <button onClick={() => fileInputRef.current.click()} className="file-select-button">Select File</button>
          <span>{fileName}</span>
          <button onClick={handleUpload} disabled={!file} className="file-upload-button">Upload File</button>
          <textarea
            placeholder="Message Study Pal"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            ref={messageInputRef}
          />
          <button type="submit" disabled={!pdfPath || !message.trim()}>Send</button>
        </form>
      </div>
    </div>
  );
};

export default ExamPal;
