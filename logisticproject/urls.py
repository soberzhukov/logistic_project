from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('payment.urls')),
    path('api/', include('common.urls')),
    path('api/', include('order.urls')),
    path('api/', include('offer.urls')),
    path('api/', include('contract.urls')),
    path('api/', include('selection.urls')),
    path('api/', include('chat.urls'))
]
