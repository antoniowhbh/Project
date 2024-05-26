import React from 'react';
import './AboutUsHeroSection.css';

function AboutUsHeroSection() {
  return (
    <div className='hero-container'>
      <video src='/videos/about-us.mp4' autoPlay loop muted />
      <h1>ABOUT US</h1>
      <p>Learn more about our mission and values</p>
    </div>
  );
}

export default AboutUsHeroSection;
