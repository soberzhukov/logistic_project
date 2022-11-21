from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('orders', views.CRUDOrderViewSet)
router.register('orders/my', views.MyListOrdersViewSet)

urlpatterns = router.urls
