"""
URLs configuration for the reminders app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReminderViewSet

# Create a router and register the ReminderViewSet with it
router = DefaultRouter()
app_name = 'reminders'
router.register(r'reminders', ReminderViewSet, basename='reminder')

urlpatterns = [
    path('', include(router.urls)),
]
