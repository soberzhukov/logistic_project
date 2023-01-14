from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('search', views.SearchViewSet)

urlpatterns = [
    path('file/save/', views.SaveFileAPIView.as_view(), name='save_file'),
] + router.urls
