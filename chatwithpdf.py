import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import openai

os.environ["OPENAI_API_KEY"] = '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'

class DocumentChatbot:
    def __init__(self, model, pdf_path):
        self.chat_model = model
        self.loader = PyPDFLoader(pdf_path)
        self.documents = self.loader.load_and_split()
        self.faiss_index = FAISS.from_documents(self.documents, OpenAIEmbeddings())

    def search_documents(self, query, k=20):
        # Returns top k similar documents based on the query
        return self.faiss_index.similarity_search(query, k)

    def chat(self, query, history=[]):
        # Search for relevant documents to use as context
        docs = self.search_documents(query)
        context = ""
        for doc in docs[:10]:  # Customize the number of documents as needed
            context += str(doc.metadata["page"]) + doc.page_content[:300] + " "

        # Create a list of messages from history and append the current query with context
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        messages.extend([{"role": role, "content": content} for role, content in history])
        messages.append({"role": "user", "content": query})
        messages.append({"role": "assistant", "content": context})

        response = openai.chat.completions.create(
            model=self.chat_model,
            messages=messages,
            max_tokens=4096
        )

        # Extract and return the chat response, and append it to history
        chat_response = response.choices[0].message.content
        history.append(("user", query))
        history.append(("assistant", chat_response))
        return chat_response

chatpdf = DocumentChatbot(model="gpt-3.5-turbo-0125",
                          pdf_path="/Users/antoniowehbe/Desktop/NDU_catalog_folder/4d98e0e5-0918-4a24-86e6-664b9ee0ed11.pdf")


def chatbot():
    history = []
    while True:
        user_message = input("You: ")
        if user_message.lower() == "quit":
            print("Chatbot session ended.")
            break
        response = chatpdf.chat(user_message, history)
        print("Chatbot:", response)

if __name__ == "__main__":
    chatbot()


