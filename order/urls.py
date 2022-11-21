from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()


router.register('orders', views.CRUDOrderViewSet)

urlpatterns = [
    path('orders/create/', views.CreateOrderAPIView.as_view()),
    path('orders/my/', views.MyListOrdersAPIView.as_view())
] + router.urls
