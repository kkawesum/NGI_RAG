from django.urls import path
from .views import chatbot_response
from . import views

urlpatterns = [
    path("", chatbot_response, name="chatbot"),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
]
