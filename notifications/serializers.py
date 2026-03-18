from rest_framework import serializers
from .models import Notification, UserNotification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'notification_type', 'created_by', 'created_at', 'is_active']

class UserNotificationSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer()

    class Meta:
        model = UserNotification
        fields = ['id', 'notification', 'is_read', 'read_at', 'created_at']