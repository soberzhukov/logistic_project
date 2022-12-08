from django.urls import path

from . import views

urlpatterns = [
    path('payment_method/', views.PaymentMethodListAPIView.as_view(), name='payment_method_list'),
    path('currency/', views.CurrencyListAPIView.as_view(), name='currency_list'),

]
