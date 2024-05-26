import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import openai
from langchain.document_loaders import UnstructuredPowerPointLoader

os.environ["OPENAI_API_KEY"] = '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'


class DocumentChatbot:
    SUPPORTED_DOCUMENT_TYPES = {
        'pdf': PyPDFLoader,
        'docx': Docx2txtLoader,
        'pptx': UnstructuredPowerPointLoader
    }

    def __init__(self, model, document_path, document_type='pdf'):
        self.chat_model = model
        self.document_type = document_type
        self.document_path = document_path
        self.validate_document_type()
        self.documents = self.load_documents()
        self.faiss_index = FAISS.from_documents(self.documents, OpenAIEmbeddings())

    def validate_document_type(self):
        if self.document_type not in self.SUPPORTED_DOCUMENT_TYPES:
            raise ValueError(f"Unsupported document type: {self.document_type}. Use one of {list(self.SUPPORTED_DOCUMENT_TYPES.keys())}.")

    def load_documents(self):
        loader_class = self.SUPPORTED_DOCUMENT_TYPES[self.document_type]
        loader = loader_class(self.document_path)
        return loader.load_and_split()

    def search_documents(self, query, k=20):
        # Returns top k similar documents based on the query
        return self.faiss_index.similarity_search(query, k)

    def chat(self, query, history=[]):
        # Search for relevant documents to use as context
        docs = self.search_documents(query)
        context = ""
        for doc in docs[:10]:  # Customize the number of documents as needed
            context += str(doc.metadata.get("page", "Slide")) + doc.page_content[:300] + " "

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


# Example usage
chatpdf = DocumentChatbot(model="gpt-3.5-turbo-0125",
                          document_path="/Users/antoniowehbe/Downloads/Modula.pptx",
                          document_type='pptx')  # Specify 'pptx' for PowerPoint files


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
