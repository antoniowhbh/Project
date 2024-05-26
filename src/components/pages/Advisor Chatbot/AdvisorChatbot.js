import React, { useState, useEffect, useRef } from 'react';
import './AdvisorChatbot.css';

const AdvisorChatbot = () => {
  const [message, setMessage] = useState('');
  const [chatResponses, setChatResponses] = useState([]);
  const messageInputRef = useRef(null);
  const chatEndRef = useRef(null);

  const sendMessage = () => {
    if (!message) return;
    appendMessage('You', message);
    fetch('http://localhost:5000/chat/message', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
      credentials: 'include'  // Include cookies with the request
    }).then(response => response.json())
      .then(data => {
        appendMessage('Helper', data.data);
      }).catch(error => {
        console.error('Error:', error);
        appendMessage('Helper', 'Error communicating with the server.');
      });
    setMessage('');  // Clear the message input after sending
  };
  
  const saveConversation = () => {
    fetch('http://localhost:5000/chat/save_conversation', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ student_id: 1 }), // Example student ID
      credentials: 'include'  // Include cookies with the request
    }).then(response => response.json())
      .then(data => {
        appendMessage('Helper', data.data); // Show success message
      }).catch(error => {
        console.error('Error:', error);
        appendMessage('Helper', 'Error saving the conversation.');
      });
  };

  const appendMessage = (sender, text) => {
    setChatResponses(prevResponses => [...prevResponses, { sender, text }]);
  };

  useEffect(() => {
    const chatEnd = chatEndRef.current;
    if (chatEnd) {
      chatEnd.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chatResponses]);

  return (
    <div className="chatbot-container">
      <div className="chat-section">
        {chatResponses.length === 0 && (
          <div className="welcome-message">
            <h1>How can I help you today?</h1>
          </div>
        )}
        <div className="chat-responses">
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
            type="text"
            id="messageInput"
            placeholder="Message Uniguide Advisor"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            ref={messageInputRef}
          />
          <button type="submit">Send</button>
          <button type="button" onClick={saveConversation}>Save Conversation</button>
        </form>
      </div>
    </div>
  );
};

export default AdvisorChatbot;
