import openai
import tiktoken
from sqlbot import CourseScheduler
from find_eligeble_courses import StudentManager
from datasource import CourseGuidelinesManager
from course_data import CourseManager
from vectordatabases import DataCollectionManager
from advisorbot import AdvisorBot
from summarizer import setup_conversation_memory, add_messages_to_history

api_key='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'
openai.api_key=api_key
EMBEDDING_MODEL = "text-embedding-3-small"

datamanager = DataCollectionManager(api_key,EMBEDDING_MODEL)

guidelines_data_collection= datamanager.create_collection('gudilines_data_collection')
course_descriptions_collection=datamanager.create_collection('course_descriptions_collection')

guidelines_manager = CourseGuidelinesManager()
guidelines_manager.load_guidelines()
guidelines_manager.add_ids_to_titles()
guidelines_ids = guidelines_manager.get_ids_as_array()
guidelines_metadata = guidelines_manager.title_dicts
guidelines_documents = guidelines_manager.guidelines

course_manager = CourseManager('course_descriptions.txt')
course_manager.load_courses()
course_manager.assign_ids()
courses_metadata = course_manager.get_course_details()
courses_documents = course_manager.get_course_descriptions()
courses_ids = course_manager.get_course_ids()

datamanager.add_documents_to_collection(guidelines_data_collection,guidelines_documents,guidelines_metadata,guidelines_ids)
datamanager.add_documents_to_collection(course_descriptions_collection,courses_documents,courses_metadata,courses_ids)

student_id=4
standing='sophomore'

studentmanager = StudentManager()

student_info= studentmanager.get_student_info(student_id)
course_list=studentmanager.full_find_eligible_courses(student_id,standing)

course_scheduler=CourseScheduler()

SYSTEM_TEMPLATE = """
Be a university advisor for the department of computer science. Your role is to answer a broad range of questions the student may have and select the right courses for the student to take. When creating a scheduel for the student take into consideration time constraints ,available seats and other factors. The student is only allowed to take one course from each group in the liberal arts curriculum.
Answer the student's questions based on the below context. 
Do not answer questions unrelated to university advisor duties.
If the context doesn't contain any relevant information to the question, don't make something up and just say "I don't know":

<context>
{context}
</context>
"""
LLM_MODEL_NAME = "gpt-3.5-turbo-0125"
ENCODING_MODEL_NAME = "cl100k_base"

encoding = tiktoken.get_encoding("cl100k_base")

advisor_bot = AdvisorBot(llm_model_name=LLM_MODEL_NAME, system_template=SYSTEM_TEMPLATE,guidelines_data_collection=guidelines_data_collection,course_description_collection=course_descriptions_collection,student_info=student_info,course_list=course_list)
def chatbot():
    history = []
    while True:
        user_message = input("You: ")
        if user_message.lower() == "quit":
            print("Chatbot session ended.")
            break
        if user_message.lower() == "confirm registration":
            confirm = input("Please enter 'confirm' to proceed: ")
            if confirm.lower() == "confirm":
                final_input=""
                generated_input=advisor_bot.answer("give me the final schedule in tabular format, without any extra information like this, don't write anything else, only the table:\n| Course Code | Course Name                         | Schedule         | Credits |", history)
                for chunk in generated_input:
                    content = chunk.choices[0].delta.content if chunk.choices[0].delta.content is not None else ""
                    final_input += content
                course_scheduler.schedule_class(f"Insert the following classes{final_input}")
                print("Registration Submitted")
            else:
                print("Registration cancelled.")
        else:
            response = advisor_bot.answer(user_message, history)
            full_response = ""  # Initialize a string to accumulate the full response
            print("Chatbot:", end=" ")  # Start the Chatbot's response line
            # Iterate over each chunk in the response
            for chunk in response:
                content = chunk.choices[0].delta.content if chunk.choices[0].delta.content is not None else ""
                full_response += content  # Append each chunk's content to the full response, ensuring it's not None
                print(content, end="")  # Print each chunk immediately, ensuring it's not None
            print("\n")
            history.append((user_message, full_response))

    updated_history=add_messages_to_history(history)
    print(setup_conversation_memory(updated_history).buffer)

if __name__ == "__main__":
    chatbot()