from django.shortcuts import render
from django.http import JsonResponse
import openai
from transformers import pipeline

api_key = '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'
openai.api_key = api_key

def ask_llm(message):
    
    # chatbot = pipeline("text-generation", model="meta-llama/Llama-2-7b-chat-hf")
    # print(chatbot(message))

    response = openai.Completion.create(
        model = "gpt-3-turbo",
        prompt = message,
        max_tokens = 150,
        n = 1,
        stop = None,
        temperature = 0.7,
    )
    print(response)
    answer = response.choices[0].text.strip()
    return answer

# Create your views here.
def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_llm(message)
        return JsonResponse({'message':message, 'response':response})
    return render(request,'chatbot.html')