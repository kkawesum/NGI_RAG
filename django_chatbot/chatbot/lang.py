from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
open_ai_key = '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'
loader = TextLoader("data.txt") #knowledgebase
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=500,chunk_overlap=50)
texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings(openai_api_key = open_ai_key)
vector_store = FAISS.from_documents(texts,embeddings)

vector_store.save_local("faiss_index")
