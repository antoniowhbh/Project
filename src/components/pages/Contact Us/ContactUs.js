import React from 'react';
import './ContactUs.css'; // Correct path within the same directory
import ContactHeroSection from './ContactHeroSection';
import ContactForm from './ContactForm';
import Footer from '../../Footer'; // Assuming Footer.js is directly in components



function ContactUs() {
  return (
    <>
      <ContactHeroSection />
      <ContactForm />
      <Footer/>
    </>
  );
}

export default ContactUs;
