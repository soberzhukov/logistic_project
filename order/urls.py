from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('orders/elected', views.ElectedOrderViewSet)
router.register('orders', views.CRUDOrderViewSet)
router.register('search', views.SearchViewSet)


urlpatterns = [
    path('orders/create/', views.CreateOrderAPIView.as_view()),
    path('orders/my/', views.MyListOrdersAPIView.as_view()),
    path('orders/<slug:pk>/view/', views.CounterOrderAPIView.as_view(), name='counter_views_order'),
] + router.urls
