class CourseManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.courses = []
        self.course_descriptions = []

    def load_courses(self):
        """Loads and parses course data from the specified file."""
        try:
            with open(self.file_path, 'r') as file:
                content = file.read()

            courses_raw = content.split('-----------------------------------------------------------------------------------------------------------------')

            for course in courses_raw:
                course = course.strip()
                if course:
                    end_index = course.index(':', course.index(':') + 1)
                    full_title = course[:end_index].strip()
                    name = full_title.split(':')[0].strip()
                    description_with_classes = course[end_index + 1:].strip()

                    description_parts = description_with_classes.split('Available classes for this course:')
                    description = description_parts[0].strip()
                    class_details = description_parts[1].strip() if len(description_parts) > 1 else ""

                    self.courses.append({"name": name, "full_title": full_title, "description": description, "class_details": class_details})
                    self.course_descriptions.append(f"{full_title}: {description}\nAvailable classes for this course: {class_details}")

        except FileNotFoundError:
            print(f"File {self.file_path} not found.")

    def assign_ids(self):
        """Assigns unique IDs to each course."""
        for i, course in enumerate(self.courses):
            course['id'] = str(i)

    def get_course_details(self):
        """Returns the list of all courses with details."""
        return self.courses

    def get_course_descriptions(self):
        """Returns formatted string descriptions of all courses."""
        return self.course_descriptions

    def get_course_ids(self):
        """Returns a list of course IDs."""
        return [course['id'] for course in self.courses]

    def get_course_names_and_titles(self):
        """Returns the list of available course codes appended with titles."""
        return [course['full_title'] for course in self.courses]


# Example usage
manager = CourseManager('course_descriptions.txt')
manager.load_courses()
course_names_and_titles = manager.get_course_names_and_titles()
# print(course_names_and_titles)