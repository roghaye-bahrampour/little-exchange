from django.urls import path, include
from rest_framework.routers import DefaultRouter

from portfolio_management.views import OrderViewSet

router = DefaultRouter()

router.register('orders', OrderViewSet, basename='base-order')


asset_urls = [
    path('', include((router.urls, 'portfolios'), namespace='portfolio')),
]