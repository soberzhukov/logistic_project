from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('offers', views.CRUDOfferViewSet)

urlpatterns = [
    path('offers/create/', views.CreateOfferAPIView.as_view()),
    path('offers/my/', views.MyListOffersAPIView.as_view()),
    path('offers/<slug:pk>/view/', views.CounterOfferAPIView.as_view(), name='counter_views_offer'),
] + router.urls
