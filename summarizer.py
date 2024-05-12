from langchain.memory import ConversationSummaryMemory, ChatMessageHistory
from langchain_openai import OpenAI
import os
os.environ["OPENAI_API_KEY"] = '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'
def setup_conversation_memory(history):
    # Ensure the OpenAI API key is set securely

    # Initialize the language model from OpenAI with a specified temperature
    llm = OpenAI(temperature=0)

    # Create a ConversationSummaryMemory instance using the provided history
    memory = ConversationSummaryMemory.from_messages(
        llm=llm,
        chat_memory=history,
        return_messages=True
    )

    # Depending on what you want to do next, you might want to return or use memory
    return memory

# # print(memory_instance.buffer)
# def convert_dialogue_format(dialogues):
#     """
#     Converts a list of dialogue tuples into a specified dictionary format.
#
#     Args:
#         dialogues (list of tuples): Each tuple contains two strings, the user input and the response.
#
#     Returns:
#         list of dicts: List where each entry is a dictionary with 'input' and 'output' keys.
#     """
#     formatted_dialogues = []
#     for user_input, response in dialogues:
#         # Create a dictionary with the specified format and append to the result list
#         formatted_dict = {"input": user_input, "output": response}
#         formatted_dialogues.append(formatted_dict)
#
#     return formatted_dialogues

def add_messages_to_history(messages):
    history = ChatMessageHistory()
    for user_msg, ai_msg in messages:
        history.add_user_message(user_msg)
        history.add_ai_message(ai_msg)
    return history
# memory = ConversationSummaryMemory.from_messages(
#     llm=OpenAI(temperature=0),
#     chat_memory=history,
#     return_messages=True
# )
#
# print(memory.buffer)