from .models import Notification
def notification_count(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(is_read = False).order_by('-updated_at')
        return {
            'notifications': notifications,
            'notification_count': notifications.count()
        }
    return {
        'notifications': [],
        'notification_count': 0
    }