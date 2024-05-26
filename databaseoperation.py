import sqlite3
from course_data import CourseManager  # Make sure to have the CourseManager class available

def insert_courses_into_database(file_path, db_name):
    # Initialize the course manager with the provided file path
    course_manager = CourseManager(file_path)
    course_manager.load_courses()

    # Connect to the database
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Ensure the Classes table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Classes (
            ClassID INTEGER PRIMARY KEY,
            ClassName TEXT NOT NULL,
            ClassDescription TEXT
        )
    ''')

    # Insert courses into the database
    for course in course_manager.get_course_details():
        cursor.execute('''
            INSERT INTO Classes (ClassName, ClassDescription) VALUES (?, ?)
        ''', (course['full_title'], course['description']))

    # Commit changes and close the database connection
    connection.commit()
    connection.close()
    print("Courses have been inserted into the database.")

# Usage
insert_courses_into_database('course_descriptions.txt', 'uniguide_student.db')
