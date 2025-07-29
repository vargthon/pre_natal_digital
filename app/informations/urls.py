"""
URLs configuration for the informations app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InformationViewSet

# Create a router and register the InformationViewSet with it
router = DefaultRouter()
app_name = 'informations'
router.register(r'informations', InformationViewSet, basename='information')

urlpatterns = [
    path('', include(router.urls)),
]