import React from 'react';
import '../App.css';
import { Button } from './Button';
import './HeroSection.css';

function HeroSection() {
  return (
    <div className='hero-container'>
      <video src='/videos/home-page-2.mp4' autoPlay loop muted />
      <h1>Uniguide</h1>
      <p>The intelligent academic advisor</p>
      <div className='hero-btns'>
        <Button
          className='btns'
          buttonStyle='btn--outline'
          buttonSize='btn--large'
          link='/advisorchatbot'
        >
          Uniguide Advisor
        </Button>
        <Button
          className='btns'
          buttonStyle='btn--primary'
          buttonSize='btn--large'
          link='/ExamPal'
        >
          Study Pal<i className='' />
        </Button>
      </div>
    </div>
  );
}

export default HeroSection;
