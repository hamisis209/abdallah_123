from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api import NotificationViewSet, UserNotificationViewSet

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet)
router.register(r'user-notifications', UserNotificationViewSet)

urlpatterns = [
    path('', views.notifications_list, name='notifications'),
    path('api/', include(router.urls)),
]
