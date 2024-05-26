import React from 'react';
import './AboutUs.css'; 
import AboutUsHeroSection from './AboutUsHeroSection';
import AboutUsContent from './AboutUsContent';
import Footer from '../../Footer'; 
const AboutUs = () => {
  return (
    <div className="about-us">
      <AboutUsHeroSection />
      <AboutUsContent />
      <Footer /> 
    </div>
  );
};

export default AboutUs;
