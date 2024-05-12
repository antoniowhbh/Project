import openai

class AdvisorBot:
    def __init__(self, llm_model_name, system_template,guidelines_data_collection,course_description_collection,student_info, course_list):
        self.llm_model_name = llm_model_name
        self.system_template = system_template
        self.guidelines_data_collection = guidelines_data_collection  # Placeholder for actual data collection
        self.course_descriptions_collection = course_description_collection  # Placeholder for actual data collection
        self.student_info=student_info
        self.course_list=course_list
    def MODEL(self,messages: list) -> dict:
        """Invoke the Large Language Model with the given messages and return the response."""
        # Placeholder for invoking gpt-3.5-turbo-16k with the messages
        # This is where you format your request payload based on OpenAI's API documentation
        response = openai.chat.completions.create(
            model=self.llm_model_name,
            messages=messages,
            max_tokens=4096,
            stream=True
        )

        return response

    def answer(self, message: str, history: list[str]) -> str:
        """Answer all the questions the student is asking, including course descriptions and creating schedules."""
        # messages
        messages = []
        # - context
        messages += [{"role": "system", "content": self.system_template}]
        messages += [{"role": "system",
                      "content": f"The following is all the info you need to know about the student: {self.student_info} These are the courses that the student is allowed to take this semester, check all the timings for these courses and form schedules only using the following courses: {self.course_list}"}]

        # - history
        for user_content, assistant_content in history:
            messages += [{"role": "user", "content": user_content}]
            messages += [{"role": "assistant", "content": assistant_content}]
        # - message
        messages += [{"role": "user", "content": message}]
        if self.guidelines_data_collection and self.course_descriptions_collection:
            results_guidelines = self.guidelines_data_collection.query(query_texts=message, n_results=3)
            documents_guidelines = results_guidelines["documents"][0]
            messages[0]["content"] += "".join(documents_guidelines)

            results_courses = self.course_descriptions_collection.query(query_texts=message, n_results=25)
            documents_courses = results_courses["documents"][0]
            messages[0]["content"] += "".join(documents_courses)

        # Generate the response
        api_response = self.MODEL(messages=messages)

        return api_response

