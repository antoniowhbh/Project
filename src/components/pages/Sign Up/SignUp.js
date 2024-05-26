import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function SignUp() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        email: '',
        username: '',
        password: '',
        major: ''
    });
    const [errorMessage, setErrorMessage] = useState('');

    const handleChange = (e) => {
        const { id, value } = e.target;
        setFormData({ ...formData, [id]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:5000/registration/signup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
                credentials: 'include'  // Include cookies with the request
            });

            if (response.ok) {
                navigate('/courses');  // Redirect to courses page on successful sign-up
            } else {
                const errorData = await response.json();
                setErrorMessage(errorData.message);
            }
        } catch (error) {
            console.error('Error during signup:', error);
            setErrorMessage('Signup failed due to network error');
        }
    };

    return (
        <div className='hero-container'>
            <video src='/videos/sign-in.mp4' autoPlay loop muted />
            <h1>Uniguide</h1>
            <p>The intelligent academic advisor</p>
            <form className='sign-up-form' onSubmit={handleSubmit}>
                <input type='text' id='firstName' placeholder='First Name' value={formData.firstName} onChange={handleChange} required />
                <input type='text' id='lastName' placeholder='Last Name' value={formData.lastName} onChange={handleChange} required />
                <input type='email' id='email' placeholder='Email' value={formData.email} onChange={handleChange} required />
                <input type='text' id='username' placeholder='Username' value={formData.username} onChange={handleChange} required />
                <input type='password' id='password' placeholder='Password' value={formData.password} onChange={handleChange} required />
                <input type='text' id='major' placeholder='Major (optional)' value={formData.major} onChange={handleChange} />
                <button type='submit' className='btn btn--primary btn--large'>Sign Up</button>
            </form>
            {errorMessage && <p className='error-message'>{errorMessage}</p>}
            <p className='sign-up-link'>
                Already a user? <a href='/login'>Log in here</a>
            </p>
        </div>
    );
}

export default SignUp;
