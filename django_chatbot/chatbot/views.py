from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render,redirect
from .utils import generate_rag_response,create_vector_store
from .models import Chat
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



vector_store = create_vector_store()
# @login_required
@csrf_exempt
def chatbot_response(request):
    try:
        if request.method == "POST":
            # ✅ Extract message safely from form data
            # chats = Chat.objects.filter(user=request.user)
            print(request.user, request.POST.get('messages'))
            message = request.POST.get('messages')
            response = generate_rag_response(message)        
            chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
            chat.save()
            return JsonResponse({'message': message, 'response': response})
        else:
            return render(request, 'chatbot.html')
            
            # if not user_query:
            #     return JsonResponse({"error": "Empty query"}, status=400)

            # ✅ Generate response

            
            
    except Exception as e:
        print("Error:", str(e))
        return JsonResponse({"error": "Something went wrong"}, status=500)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Error creating account'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Password dont match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

