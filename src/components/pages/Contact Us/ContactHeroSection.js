import React from 'react';
import './ContactHeroSection.css';

function ContactHeroSection() {
  return (
    <div className='hero-container'>
      <video src='/videos/contact-us.mp4' autoPlay loop muted />
      <h1>Contact US</h1>
      <p>We'd love to hear from you!</p>
    </div>
  );
}

export default ContactHeroSection;
