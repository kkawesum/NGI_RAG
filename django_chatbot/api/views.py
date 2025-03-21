from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render,redirect
from chatbot.utils import generate_rag_response,create_vector_store
from .models import Chat
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required




@csrf_exempt
def hello_world(request):
    try:
        if request.method == "POST":
            # ✅ Extract message safely from form data
            # chats = Chat.objects.filter(user=request.user)
            print(request.user)
            message = request.POST.get('message')
            response = generate_rag_response(message)        
            chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
            chat.save()
            return JsonResponse({'message': message, 'response': response})
        else:
            return render(request, 'index.html')
            
            # if not user_query:
            #     return JsonResponse({"error": "Empty query"}, status=400)

            # ✅ Generate response

            
            
    except Exception as e:
        print("Error:", str(e))
        return JsonResponse({"error": "Something went wrong"}, status=500)
