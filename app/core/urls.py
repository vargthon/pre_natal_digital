"""
URLs for core app
"""
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from core import views

from rest_framework import routers

app_name = 'core'

router = routers.DefaultRouter()
router.register(
    'users',
    views.UserViewSet,
    basename='user')
router.register(
    'admin/users',
    views.AdminUserViewSet,
    basename='admin-user')

router.register(
    'admin/user-profiles',
    views.UserProfileModelView,
    basename='user-profile')


urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('token/verify/', TokenVerifyView.as_view(), name='verify-token'),
    path('detail/me/', views.MeView.as_view(), name='me'),
    path('user-profiles/', views.UserProfileUpdateView.as_view(),
         name='user-profile-update'),
    path('user-profiles/me', views.UserProfileView.as_view(),
         name='user-profile-view'),
    path('user-profiles/image-upload',
         views.UserProfileImageUploadView.as_view(),
         name='image-upload'),
]
