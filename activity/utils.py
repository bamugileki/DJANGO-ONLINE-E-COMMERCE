from .models import ActivityLog


def log_activity(request, action, model_name='', object_id=None, description=''):
    user = request.user if request.user.is_authenticated else None
    ip_address = request.META.get('REMOTE_ADDR', '')
    ActivityLog.objects.create(
        user=user,
        action=action,
        model_name=model_name,
        object_id=object_id,
        description=description,
        ip_address=ip_address,
    )
