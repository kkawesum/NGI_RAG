from django.urls import path
from .views import get_csrf_token, hello_world

urlpatterns = [
    path('', hello_world,name='chatbot'),
    path("csrf/", get_csrf_token, name="csrf"),

    
]
