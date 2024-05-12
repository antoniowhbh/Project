import openai
import chromadb
import datasource
import course_data
import tiktoken
import find_eligeble_courses
from sqlbot import schedule_class


# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_API_KEY"] = getpass.getpass()


openai.api_key='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'

# I've set this to our new embeddings model, this can be changed to the embedding model of your choice
EMBEDDING_MODEL = "text-embedding-3-small"
chroma_client = chromadb.EphemeralClient()
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction


embedding_function = OpenAIEmbeddingFunction(api_key=openai.api_key, model_name=EMBEDDING_MODEL)

guidelines_data_collection = chroma_client.create_collection(name='guidelines_data_collection', embedding_function=embedding_function)
course_descriptions_collection = chroma_client.create_collection(name='course_descriptions_collection', embedding_function=embedding_function)

guidelines_data_collection.add(
    documents=datasource.guidelines,
    metadatas=datasource.title_dicts,
    ids=datasource.ids

)

course_descriptions_collection.add(
    documents=course_data.course_descriptions,
    metadatas=course_data.courses,
    ids=course_data.ids

)
student_id=4
standing='sophomore'
student_info=find_eligeble_courses.get_student_info(student_id)
course_list=find_eligeble_courses.find_eligible_courses(student_id,standing)
SYSTEM_TEMPLATE = """
Be a university advisor for the department of computer science. Your role is to answer a broad range of questions the student may have and select the right courses for the student to take. When creating a scheduel for the student take into consideration time constraints ,available seats and other factors. The student is only allowed to take one course from each group in the liberal arts curriculum.
Answer the student's questions based on the below context. 
Do not answer questions unrelated to university advisor duties.
If the context doesn't contain any relevant information to the question, don't make something up and just say "I don't know":

<context>
{context}
</context>
"""
LLM_MODEL_NAME = "gpt-4-turbo"
ENCODING_MODEL_NAME = "cl100k_base"

encoding = tiktoken.get_encoding("cl100k_base")
def MODEL(messages: list) -> dict:
    """Invoke the Large Language Model with the given messages and return the response."""
    # Placeholder for invoking gpt-3.5-turbo-16k with the messages
    # This is where you format your request payload based on OpenAI's API documentation
    response = openai.chat.completions.create(
        model=LLM_MODEL_NAME,
        messages=messages,
        max_tokens=4096,
        stream=True
    )

    return response


def answer(message: str, history: list[str]) -> str:
    """Answer all the questions the student is asking, including course descriptions and creating schedules."""
    # messages
    messages = []
    # - context
    messages += [{"role": "system", "content": SYSTEM_TEMPLATE}]
    messages += [{"role":"system", "content": f"The following is all the info you need to know about the student: {student_info} These are the courses that the student is allowed to take this semester, check all the timings for these courses and form schedules only using the following courses: {course_list}"}]

    # - history
    for user_content, assistant_content in history:
        messages += [{"role": "user", "content": user_content}]
        messages += [{"role": "assistant", "content": assistant_content}]
    # - message
    messages += [{"role": "user", "content": message}]

    # Query the first database (guidelines_data_collection)
    results_guidelines = guidelines_data_collection.query(query_texts=message, n_results=3)
    documents_guidelines = results_guidelines["documents"][0]
    messages[0]["content"] += "".join(documents_guidelines)

    # Query the second database (course_description_collection)
    results_courses = course_descriptions_collection.query(query_texts=message, n_results=20)
    documents_courses = results_courses["documents"][0]
    messages[0]["content"] += "".join(documents_courses)

    # Generate the response
    api_response = MODEL(messages=messages)

    return api_response
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
                generated_input=answer("give me the final schedule in tabular format, without any extra information like this:\n| Course Code | Course Name                         | Schedule         | Credits |", history)
                for chunk in generated_input:
                    content = chunk.choices[0].delta.content if chunk.choices[0].delta.content is not None else ""
                    final_input += content
                schedule_class(f"Insert the following classes{final_input}")
                print("Registration Submitted")
            else:
                print("Registration cancelled.")
        else:
            response = answer(user_message, history)
            full_response = ""  # Initialize a string to accumulate the full response
            print("Chatbot:", end=" ")  # Start the Chatbot's response line
            # Iterate over each chunk in the response
            for chunk in response:
                content = chunk.choices[0].delta.content if chunk.choices[0].delta.content is not None else ""
                full_response += content  # Append each chunk's content to the full response, ensuring it's not None
                print(content, end="")  # Print each chunk immediately, ensuring it's not None
            print("\n")
            history.append((user_message, full_response))

if __name__ == "__main__":
    chatbot()