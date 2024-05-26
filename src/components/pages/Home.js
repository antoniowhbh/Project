import React from 'react';
import '../../App.css';
import Cards from '../Cards';
import HeroSection from '../HeroSection';
import FAQ from '../FAQ'; 
import Footer from '../Footer';

function Home() {
  return (
    <>
      <HeroSection />
      <Cards />
      <FAQ />
      <Footer />
    </>
  );
}

export default Home;
