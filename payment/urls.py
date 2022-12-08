from django.urls import path

from . import views

urlpatterns = [
    path('payment_method/', views.PaymentMethodListAPIView.as_view(), name='payment_method_list'),


]
