from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('search', views.SearchViewSet)

urlpatterns = [
    path('image/save/', views.SaveImageAPIView.as_view(), name='save_image'),
] + router.urls
