from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import generate_rag_response,create_vector_store

@csrf_exempt
def chatbot_response(request):
    create_vector_store()
    if request.method == "POST":
        data = json.loads(request.body)
        user_query = data.get("message", "")

        response = generate_rag_response(user_query)
        
        return JsonResponse({"response": response})
    
    return JsonResponse({"error": "Invalid request"}, status=400)
