from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserActivityViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('activities', UserActivityViewSet, basename='useractivities')

urlpatterns = [
    path('', include(router.urls)),
]