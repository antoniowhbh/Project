import React, { useState } from 'react';
import { useContext } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import AuthContext from './AuthContext.js';
import './SignIn.css';

function SignIn() {
    const { login } = useContext(AuthContext); // Use login instead of setIsAuthenticated
    const navigate = useNavigate();
    const location = useLocation();
    const { from } = location.state || { from: { pathname: '/' } }; // Default to home if no redirect path
    const [formData, setFormData] = useState({ username: '', password: '' });
    const [errorMessage, setErrorMessage] = useState('');

    const handleChange = (e) => {
      const { id, value } = e.target;
      setFormData({ ...formData, [id]: value });
    };

    const handleSubmit = async (e) => {
      e.preventDefault();
      try {
        const response = await fetch('http://localhost:5000/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData),
          credentials: 'include'
        });
  
        if (response.ok) {
          const data = await response.json();
          if (data.status === 'success') {
            login(); // Call login instead of setIsAuthenticated
            navigate(from.pathname); 
            // Navigate to the page they were trying to access
          } else {
            setErrorMessage(data.message);
          }
        } else {
          console.error('HTTP error:', response.status);
          setErrorMessage('Login failed due to server error');
        }
      } catch (error) {
        console.error('Error during login:', error);
        setErrorMessage('Login failed due to network error');
      }
    };
    return (
        <div className='hero-container'>
            <video src='/videos/sign-in.mp4' autoPlay loop muted />
            <h1>Uniguide</h1>
            <p>The intelligent academic advisor</p>
            <form className='sign-in-form' onSubmit={handleSubmit}>
                <input 
                    type='text' 
                    id='username' 
                    placeholder='Username' 
                    value={formData.username} 
                    onChange={handleChange} 
                    required 
                />
                <input 
                    type='password' 
                    id='password' 
                    placeholder='Password' 
                    value={formData.password} 
                    onChange={handleChange} 
                    required 
                />
                <button type='submit' className='btn btn--primary btn--large'>
                    Sign In
                </button>
            </form>
            {errorMessage && <p className='error-message'>{errorMessage}</p>}
            <p className='sign-up-link'>
                Not a user? <a href='/sign-up'>Sign up here</a>
            </p>
        </div>
    );
}

export default SignIn;
