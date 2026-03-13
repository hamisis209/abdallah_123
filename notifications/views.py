from django.shortcuts import render

def notifications_list(request):
    # Placeholder data; replace with real notifications model/query.
    notifications = [
        {'title': 'Welcome', 'body': 'Thanks for joining Inclusive Learning.'},
        {'title': 'Course Updates', 'body': 'New materials are available in Mathematics.'},
    ]
    return render(request, 'notifications/notifications.html', {'notifications': notifications})
