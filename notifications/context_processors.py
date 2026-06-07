from .models import Notification


def notifications(request):
    if request.user.is_authenticated:
        recent = Notification.objects.filter(user=request.user)[:5]
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    else:
        recent = []
        unread_count = 0
    return {
        'recent_notifications': recent,
        'unread_notifications_count': unread_count,
    }
