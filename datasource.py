class CourseGuidelinesManager:
    def __init__(self, file_path='course_guidelines.txt'):
        self.file_path = file_path
        self.delimiter = "-" * 125  # Adjust the number of hyphens as per your file
        self.title_dicts = []  # This will hold the title dictionaries
        self.guidelines = []  # This will hold the guideline texts

    def load_guidelines(self):
        """Loads and parses the course guidelines from the specified file."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                sections = file.read().split(self.delimiter)
                self._parse_sections(sections)
        except FileNotFoundError:
            print(f"File {self.file_path} not found.")

    def _parse_sections(self, sections):
        """Parses each section of the file to extract titles and guidelines."""
        for section in sections:
            start_quote_index = section.find('"')
            end_quote_index = section.find('"', start_quote_index + 1)

            if start_quote_index != -1 and end_quote_index != -1:
                title = section[start_quote_index + 1:end_quote_index]
                guideline = section[end_quote_index + 1:].strip()
                self.title_dicts.append({"title": title})
                self.guidelines.append(guideline)

    def add_ids_to_titles(self):
        """Assigns a unique ID to each title dictionary."""
        ids = [str(i) for i in range(len(self.guidelines))]
        for i, title_dict in enumerate(self.title_dicts):
            title_dict['id'] = ids[i]

    def get_ids_as_array(self):
        """Returns an array of string IDs."""
        return [title_dict['id'] for title_dict in self.title_dicts]


