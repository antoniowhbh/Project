
import React, { createContext, useContext, useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import Navbar from './components/Navbar';
import './App.css';
import Home from './components/pages/Home';
import SignUp from './components/pages/Sign Up/SignUp';
import SignIn from './components/pages/Sign In/SignIn';
import AboutUs from './components/pages/About Us/AboutUs';
import ContactUs from './components/pages/Contact Us/ContactUs';
import Notes from './components/pages/Notes/Notes';
import ExamPal from './components/pages/Exam Pal/ExamPal';
import AdvisorChatbot from './components/pages/Advisor Chatbot/AdvisorChatbot';
import SavedConversation from './components/pages/Archived Chats/SavedConversation';
import CourseSelection from './components/pages/courses/courses';
import { AuthProvider } from './components/pages/Sign In/AuthContext';
import AuthContext from './components/pages/Sign In/AuthContext'; 


// A component to protect private routes
const PrivateRoute = ({ children }) => {
  const { isAuthenticated } = useContext(AuthContext);
  const location = useLocation();

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Navbar />
        <Routes>
          <Route path='/' element={<Home />} />
          <Route path='/login' element={<SignIn />} />
          <Route path='/sign-up' element={<SignUp />} />
          <Route path='/about-us' element={<AboutUs />} />
          <Route path='/contact-us' element={<ContactUs />} />
          <Route path='/notes' element={<PrivateRoute><Notes /></PrivateRoute>} />
          <Route path='/ExamPal' element={<PrivateRoute><ExamPal /></PrivateRoute>} />
          <Route path='/advisorchatbot' element={<PrivateRoute><AdvisorChatbot /></PrivateRoute>} />
          <Route path='/saved-conversations' element={<PrivateRoute><SavedConversation /></PrivateRoute>} />
          <Route path='/courses' element={<PrivateRoute><CourseSelection /></PrivateRoute>} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
