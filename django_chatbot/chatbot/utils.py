import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from sentence_transformers import SentenceTransformer




# Get base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define file path
KNOWLEDGE_FILE = os.path.join(BASE_DIR, "chatbot", "doc", "knowledge_base.txt")

# def load_knowledge_base():
#     """Loads the knowledge base from the file."""
#     if not os.path.exists(KNOWLEDGE_FILE):
#         raise FileNotFoundError(f"Error: The file '{KNOWLEDGE_FILE}' does not exist.")
    
#     with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as file:
#         return file.read()

# # Test if the function works
# if __name__ == "__main__":
#     print(load_knowledge_base())  # Run this in a Python shell


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load and split documents for retrieval
def load_documents():
    loader = TextLoader(KNOWLEDGE_FILE)  # Load from file
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    return docs

# Create vector database for retrieval
def create_vector_store():
    docs = load_documents()
    model = SentenceTransformer("all-MiniLM-L6-v2")  # Lightweight and fast
    embedding = model.encode(docs)

    vectorstore = FAISS.from_documents(docs, embedding)
    return vectorstore

vector_store = create_vector_store()

# Generate response using RAG
def generate_rag_response(user_query):
    # Retrieve relevant documents
    relevant_docs = vector_store.similarity_search(user_query, k=3)
    context = " ".join([doc.page_content for doc in relevant_docs])

    # Query Gemini API
    response = genai.GenerativeModel("gemini-pro").generate_content(f"Context: {context}\nUser: {user_query}")
    
    return response.text
