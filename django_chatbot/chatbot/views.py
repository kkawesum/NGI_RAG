from django.shortcuts import render
from django.http import JsonResponse

from django.conf import settings
import google.generativeai as genai
from transformers import pipeline
from langchain_community.vectorstores.faiss import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

open_ai_key = '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'
genai.configure(api_key=settings.GEMINI_API_KEY)

vector_store = FAISS.load_local("faiss_index", OpenAIEmbeddings(openai_api_key=open_ai_key),allow_dangerous_deserialization=True)
# Create your views here.
def chatbot(request):
    user_input = request.GET.get("message","")

    docs = vector_store.similarity_search(user_input,k=3)
    context = " ".join([doc.page_content for doc in docs])

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(f"Context:{context}\n\n User:{user_input}\nAI:")

    return JsonResponse({"response":response.text})