from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('contract', views.CreateReadContractViewSet)

urlpatterns = [
    path('contract/<slug:pk>/status/', views.ChangeStatusAPIView.as_view()),
] + router.urls
