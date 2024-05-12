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
                    end_index = course.index(':')
                    name = course[:end_index].strip()
                    description_with_classes = course[end_index + 1:].strip()

                    description_parts = description_with_classes.split('Available classes for this course:')
                    description = description_parts[0].strip()
                    class_details = description_parts[1].strip() if len(description_parts) > 1 else ""

                    self.courses.append({"name": name, "description": description, "class_details": class_details})
                    self.course_descriptions.append(f"{name}: {description}\nAvailable classes for this course: {class_details}")

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

