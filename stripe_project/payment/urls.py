from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ItemsViewSet, OrderViewSet, create_checkout


router = DefaultRouter()
router.register(r'items', ItemsViewSet, basename='items')
router.register(r'order', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('buy/<pk>/', create_checkout)
]
