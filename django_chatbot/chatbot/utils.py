import os
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# Get base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define file path
KNOWLEDGE_FILE = os.path.join(BASE_DIR, "chatbot", "doc", "knowledge_base.txt")

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load and split documents
def load_documents():
    loader = TextLoader(KNOWLEDGE_FILE)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    return docs

# Create vector database for retrieval
def create_vector_store():
    docs = load_documents()
    
    # ✅ Extract text from Documents
    texts = [doc.page_content for doc in docs]

    # ✅ Use HuggingFace embeddings
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # ✅ Create FAISS vector store
    vectorstore = FAISS.from_texts(texts, embedding_model)
    return vectorstore

# ✅ Create the FAISS vector store
vector_store = create_vector_store()

# Generate response using RAG
def generate_rag_response(user_query):
    # Retrieve relevant documents
    relevant_docs = vector_store.similarity_search(user_query, k=3)

    print(type(relevant_docs))  # Should print <class 'list'>
    print(relevant_docs)  # See the full object structure

    # ✅ Extract text for Gemini
    context = " ".join([doc.page_content for doc in relevant_docs])

    # ✅ Query Gemini API
    response = genai.GenerativeModel("gemini-pro").generate_content(f"Context: {context}\nUser: {user_query}")
    
    return response.text
