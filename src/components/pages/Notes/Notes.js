import React from 'react';
import NotesHeroSection from './NotesHeroSection';
import NotesGrid from './NotesGrid';
import Footer from '../../Footer'; 

function Notes() {
  return (
    <div className="notes-page">
      <NotesHeroSection />
      <NotesGrid />
      <Footer />
    </div>
  );
}

export default Notes;
