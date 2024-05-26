import React from 'react';
import './NotesHeroSection.css';

function NotesHeroSection() {
  return (
    <div className='hero-container'>
      <video src='/videos/notes.mp4' autoPlay loop muted />
      <h1>STRESSING BEFORE YOUR EXAM ?</h1>
      <p>Find the notes you need for your courses</p>
    </div>
  );
}

export default NotesHeroSection;
