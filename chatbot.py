from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import re

# Initialize Elasticsearch client
es = Elasticsearch("http://localhost:9200")

# Load pre-trained embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Data Collection: Load and process text file
def load_text_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        text = file.read()
    return text.split("\n")  # Split into lines or paragraphs

# Preprocessing: Clean and preprocess text
def preprocess_text(text_chunks):
    cleaned_chunks = [re.sub(r'[^a-zA-Z0-9\s]', '', chunk).strip().lower() for chunk in text_chunks]
    return cleaned_chunks

# Store data: Index text in Elasticsearch
def index_data(index_name, text_chunks):
    es.indices.create(index=index_name, ignore=400)
    actions = [
        {
            "_index": index_name,
            "_id": i,
            "_source": {"text": chunk, "embedding": embed_model.encode(chunk).tolist()}
        }
        for i, chunk in enumerate(text_chunks)
    ]
    bulk(es, actions)

# Retrieval Setup: Retrieve relevant text using Elasticsearch
def retrieve_relevant_text(query, index_name, top_k=3):
    query_embedding = embed_model.encode(query).tolist()
    search_body = {
        "size": top_k,
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {"query_vector": query_embedding}
                }
            }
        }
    }
    response = es.search(index=index_name, body=search_body)
    return "\n".join([hit["_source"]["text"] for hit in response["hits"]["hits"]])

# Integration with Language Model: Generate response using retrieved context
def generate_response(query, context):
    client = OpenAI(api_key="your_openai_api_key")
    prompt = f"Context: {context}\n\nUser: {query}\nChatbot:"
    response = client.Completions.create(model="gpt-4", prompt=prompt, max_tokens=200)
    return response.choices[0].text.strip()

# Main chatbot function
def chatbot(query, index_name):
    context = retrieve_relevant_text(query, index_name)
    return generate_response(query, context)

# Example usage
if __name__ == "__main__":
    text_data = load_text_file("knowledge_base.txt")
    preprocessed_data = preprocess_text(text_data)
    index_name = "rag_index"
    index_data(index_name, preprocessed_data)
    
    user_query = "What is retrieval-augmented generation?"
    response = chatbot(user_query, index_name)
    print(response)
