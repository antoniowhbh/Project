import React, { useState, useEffect } from 'react';
import './courses.css';
import { useNavigate } from 'react-router-dom';

function CourseSelection() {
  const [courses, setCourses] = useState([]); // State to store the list of courses
  const [selectedCourses, setSelectedCourses] = useState([]); // State to store selected courses
  const [searchTerm, setSearchTerm] = useState(''); // State to store the search term
  const navigate = useNavigate();

  // Fetch courses on component mount
  useEffect(() => {
    const fetchCourses = async () => {
      const response = await fetch('http://localhost:5000/api/courses/courses');
      const data = await response.json();
      setCourses(data);
    };

    fetchCourses();
  }, []);

  // Handle course toggle
  const handleCourseToggle = (courseId) => {
    setSelectedCourses(prevSelectedCourses =>
      prevSelectedCourses.includes(courseId)
        ? prevSelectedCourses.filter(id => id !== courseId)
        : [...prevSelectedCourses, courseId]
    );
  };

  // Handle submit
  const handleSubmit = async () => {
    const response = await fetch('http://localhost:5000/api/courses/select-courses', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        student_id: 'your_student_id', // Replace 'your_student_id' with the actual student ID
        selected_courses: selectedCourses
      })
    });
    const result = await response.json();
    if (result.status === 'success') {
      navigate('/success'); // Navigate to a success page or handle success scenario
    } else {
      alert(result.message); // Show error message
    }
  };

  // Filter courses based on search term
  const filteredCourses = courses.filter(course =>
    course.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className='hero-container'>
      <video src='/videos/sign-in.mp4' autoPlay loop muted />
      <h1>Select Your Courses</h1>
      <p className='description'>
        Select all the courses you have previously taken to enhance your academic advising experience.
      </p>
      <input
        type="text"
        placeholder="Search courses..."
        onChange={e => setSearchTerm(e.target.value)}
        className="search-bar"
      />
      <div className='course-selection-container'>
        <div className='courses-list'>
          {filteredCourses.map(course => (
            <div key={course.id} className='course-item'>
              <input
                type="checkbox"
                id={`course_${course.id}`}
                checked={selectedCourses.includes(course.id)}
                onChange={() => handleCourseToggle(course.id)}
              />
              <label htmlFor={`course_${course.id}`}>{course.name}</label>
            </div>
          ))}
        </div>
        <button className='submit-button' onClick={handleSubmit}>Submit Courses</button>
      </div>
    </div>
  );
}

export default CourseSelection;
