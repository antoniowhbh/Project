import openai
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

class DataCollectionManager:
    def __init__(self, api_key, embedding_model):
        openai.api_key = api_key  # Set the API key for OpenAI
        self.embedding_model = embedding_model
        self.client = chromadb.EphemeralClient()  # Initialize the ChromaDB client
        self.embedding_function = OpenAIEmbeddingFunction(api_key=api_key, model_name=self.embedding_model)

        # Initialize collections
        # self.guidelines_data_collection = self.create_collection('guidelines_data_collection')
        # self.course_descriptions_collection = self.create_collection('course_descriptions_collection')

    def create_collection(self, name):
        """ Create a collection with the specified name using the embedding function """
        return self.client.create_collection(name=name, embedding_function=self.embedding_function)

    def add_documents_to_collection(self, collection, documents, metadatas, ids):
        """ Add documents to a specified collection """
        collection.add(documents=documents, metadatas=metadatas, ids=ids)

# Example usage:
api_key = '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'
embedding_model = "text-embedding-3-small"
manager = DataCollectionManager(api_key, embedding_model)