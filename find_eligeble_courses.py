# import sqlite3
# import json

# Ensure this database creation function is called before attempting to add students or find eligible courses
# def create_students_table():
#     conn = sqlite3.connect('studentinfo.db')
#     cursor = conn.cursor()
#     query = """
#     CREATE TABLE IF NOT EXISTS students (
#         student_id INTEGER PRIMARY KEY AUTOINCREMENT,
#         student_name TEXT NOT NULL,
#         major TEXT NOT NULL,
#         courses_taken TEXT NOT NULL
#     )
#     """
#     cursor.execute(query)
#     conn.commit()
#     conn.close()
import sqlite3
import json

class StudentManager:
    def __init__(self, db_path='studentinfo.db'):
        self.db_path = db_path

    def add_student(self, student_name, major, courses_taken):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        courses_taken_str = ', '.join(courses_taken)
        cursor.execute("INSERT INTO students (student_name, major, courses_taken) VALUES (?, ?, ?)", (student_name, major, courses_taken_str))
        conn.commit()
        conn.close()

    def generate_students(self):
        students_courses = [
            ["Alice", "BachelorOfScienceInComputerScience", ["CSC 212", "MAT 211", "CSC 219", "CSC 202", "MAT 213"]],
            # Add more students here if necessary...
        ]
        for student in students_courses:
            self.add_student(*student)

    def get_student_info(self, student_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT student_name, major, courses_taken FROM students WHERE student_id = ?", (student_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            student_name, major, courses_taken = result
            return {"Student Name": student_name, "Major": major, "Courses Taken": courses_taken.split(', ')}
        return None

    def find_eligible_courses(self, student_id, student_class_standing):
        student_info = self.get_student_info(student_id)
        if not student_info:
            print("No information found for the specified student ID.")
            return []

        major_to_file = {
            "BachelorOfScienceInComputerScience": "computerscience.txt",
            "Computer Graphics Animation": "cga.txt",
            "Information Technology": "it.txt",
            "Management of Information Systems": "mis.txt",
            "Business Computing": "businesscomputing.txt",
            "Geographic Information Systems": "gis.txt"
        }

        major = student_info["Major"]
        completed_courses = student_info["Courses Taken"]
        file_name = major_to_file.get(major)

        if not file_name:
            print("No file associated with the student's major.")
            return []

        try:
            with open(file_name, 'r') as file:
                courses_catalog = json.load(file)[major]
        except Exception as e:
            print(f"Failed to load course catalog: {e}")
            return []

        eligible_courses = []
        for category_key, category_value in courses_catalog.items():
            if category_key == "LiberalArtsCurriculum":
                for group in category_value["Groups"]:
                    for course in group["Courses"]:
                        if course["code"] in completed_courses:
                            continue
                        # Assuming prerequisites is a list or None
                        prerequisites = course.get("prerequisites", [])
                        if prerequisites is None:
                            prerequisites = []
                        prerequisites_met = all(prerequisite in completed_courses for prerequisite in prerequisites)
                        if prerequisites_met:
                            eligible_courses.append({"code": course["code"],
                                                     "category": f"Liberal Arts Curriculum - Group {group['Group']}"})
            else:
                # Other categories that are assumed to be simple lists of courses
                for course in category_value:
                    if course["code"] in completed_courses:
                        continue
                    prerequisites = course.get("prerequisites", [])
                    if prerequisites is None:
                        prerequisites = []
                    prerequisites_met = all(prerequisite in completed_courses for prerequisite in prerequisites)
                    if prerequisites_met:
                        eligible_courses.append({"code": course["code"], "category": category_key})

        return eligible_courses

    def full_find_eligible_courses(self, student_id, student_class_standing):
        eligible_courses = self.find_eligible_courses(student_id, student_class_standing)
        if not eligible_courses:
            print("No eligible courses found or an error occurred.")
            return

        # Assuming 'code' is always present in the dictionaries:
        course_codes = [course['code'] for course in eligible_courses]
        # Simulate reading from a file and getting the course titles
        course_titles = self.extract_course_titles('course_descriptions.txt')
        matched_courses = self.match_course_codes_with_names(course_titles, course_codes)
        courses_string = ', '.join(matched_courses)
        return courses_string

    def extract_course_titles(self, file_path):
        course_titles = []
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if line.strip():  # Check if the line is not empty
                        title_end_index = line.find('(')  # Find the index of '(' indicating the start of credit count
                        if title_end_index != -1:
                            course_title = line[:title_end_index].strip()  # Extract the title
                            course_titles.append(course_title)
        except FileNotFoundError:
            print("The specified file was not found.")
        return course_titles

    def match_course_codes_with_names(self, course_names, course_codes):
        matched_courses = []
        for code in course_codes:
            for name in course_names:
                if code.lower() in name.lower():  # Check if the code is part of the name
                    matched_courses.append(name)
                    break  # Break inner loop once a match is found
        return matched_courses


