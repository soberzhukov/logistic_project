from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views


urlpatterns = [
    path('chat/create/', views.CreateChatAPIView.as_view(), name='create_chat'),
]