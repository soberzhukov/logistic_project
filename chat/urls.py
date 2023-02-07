from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views


urlpatterns = [
    path('chat/create/', views.CreateChatAPIView.as_view(), name='create_chat'),
    path('chat/', views.ListChatAPIView.as_view(), name='list_chat'),
    path('chat/<slug:pk>/', views.RetrieveDeleteMainChatAPIView.as_view(), name='delete_main_chat'),
    path('chat/item/<slug:pk>/', views.GetOrDeleteChatAPIView.as_view(), name='get_or_delete_item_chat'),
    path('chat/item/<slug:pk>/message/', views.GetMessagesAPIView.as_view(), name='get_or_delete_item_chat'),
    path('chat/item/<slug:pk>/message/create/', views.CreateChatMessageAPIView.as_view(), name='create_message'),
]