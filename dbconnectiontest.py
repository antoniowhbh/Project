import sqlite3

# def create_students_table():
#     conn = sqlite3.connect('studentinfo.db')
#     cursor = conn.cursor()
#
#     # SQL query to create the students table
#     query = """
#     CREATE TABLE IF NOT EXISTS students (
#         student_id INTEGER PRIMARY KEY AUTOINCREMENT,
#         student_name TEXT NOT NULL,
#         major TEXT NOT NULL,
#         courses_taken TEXT NOT NULL
#     )
#     """
#
#     cursor.execute(query)
#     conn.commit()
#     conn.close()
#
# # Call this function to create the table before adding any students
# #create_students_table()

def add_student(student_name, major, courses_taken):
    conn = sqlite3.connect('studentinfo.db')
    cursor = conn.cursor()

    # Assuming the students table is already created with appropriate fields
    # student_id is auto-incremented, assuming it's set up as such in the DB schema
    query = """
    INSERT INTO students (student_name, major, courses_taken)
    VALUES (?, ?, ?)
    """

    # Join the courses list to a string to store in the database
    courses_taken_str = ', '.join(courses_taken)

    cursor.execute(query, (student_name, major, courses_taken_str))
    conn.commit()
    conn.close()


def generate_students():
    students_courses = [
        ["Alice", "BachelorOfScienceInComputerScience", ["CSC 212", "MAT 211", "CSC 219", "CSC 202", "MAT 213"]],
        ["Bob", "BachelorOfScienceInComputerScience",
         ["CSC 212", "CSC 213", "MAT 211", "CSC 316", "CSC 323", "MAT 215"]],
        ["Charlie", "BachelorOfScienceInComputerScience",
         ["CSC 212", "CSC 213", "CSC 313", "MAT 211", "CSC 311", "CSC 312", "MAT 224"]],
        ["Diana", "BachelorOfScienceInComputerScience",
         ["CSC 213", "CSC 313", "CSC 413", "CSC 414", "CSC 423", "MAT 326"]],
        ["Evan", "BachelorOfScienceInComputerScience",
         ["CSC 425", "CSC 426", "CSC 432", "CSC 480", "CSC 490", "CSC 457"]]
    ]

    for student_name, major, courses_taken in students_courses:
        add_student(student_name, major, courses_taken)


# Call the function to generate and add the students
generate_students()
def get_student_info(student_id):
    # Connect to your database
    conn = sqlite3.connect('studentinfo.db')  # Changed to 'school.db'
    cursor = conn.cursor()

    # SQL query to retrieve student name, major, and courses taken
    query = """
    SELECT student_name, major, courses_taken
    FROM students
    WHERE student_id = ?
    """

    # Execute the query
    cursor.execute(query, (student_id,))

    # Fetch the results
    results = cursor.fetchone()  # Changed to fetchone() as we expect a single result

    # Close the connection
    conn.close()

    # Format and return the results
    if results:
        student_name, major, courses_taken = results
        courses_list = courses_taken.split(', ')  # Assuming courses are separated by ', '
        return {"Student Name": student_name, "Major": major, "Courses Taken": courses_list}
    else:
        return "No information found for the specified student ID."

# Example usage
# student_info = get_student_info(1)  # Assuming '1' is the student_id
# print(student_info)

# Fetch and print information for a test student
# Assuming we want to fetch the information for the student with student_id = 1
test_student_info = get_student_info(1)
print(test_student_info)