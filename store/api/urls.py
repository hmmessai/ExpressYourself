from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ColorViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'colors', ColorViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
