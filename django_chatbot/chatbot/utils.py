import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load and split documents for retrieval
def load_documents():
    loader = TextLoader("knowledge_base.txt")  # Load from file
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    return docs

# Create vector database for retrieval
def create_vector_store():
    docs = load_documents()
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
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
