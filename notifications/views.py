from django.shortcuts import render
from .models import Notification, UserNotification

def notifications_list(request):
    if request.user.is_authenticated:
        # Get user's notifications
        user_notifications = UserNotification.objects.filter(
            user=request.user
        ).select_related('notification').order_by('-created_at')

        # Mark all as read
        unread_notifications = user_notifications.filter(is_read=False)
        for user_notif in unread_notifications:
            user_notif.mark_as_read()

        notifications = [un.notification for un in user_notifications]
    else:
        notifications = []

    return render(request, 'notifications/notifications.html', {
        'notifications': notifications,
        'user_notifications': user_notifications if request.user.is_authenticated else []
    })
