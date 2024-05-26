import React, { useState } from 'react';
import './NotesGrid.css';

function NotesGrid() {
  const [searchTerm, setSearchTerm] = useState('');
  const courses = [
    'CSC 423: Software Egineering',
    'CSC 311: Theory of Computation',
    'CSC 313: Data Structures',
    'MAT 213: Calculus III',
    'CSC 325: Analysis of Algorithms',
    'CSC 432: Introduction to Artificial Intelligence',
  ];

  const filteredCourses = courses.filter(course =>
    course.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className='notes-grid-container'>
      <input
        type='text'
        className='search-bar'
        placeholder='Search for a course...'
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <div className='grid'>
        {filteredCourses.map((course, index) => (
          <div key={index} className='grid-item'>
            {course}
          </div>
        ))}
      </div>
    </div>
  );
}

export default NotesGrid;
