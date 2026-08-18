from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.apps import apps
from .models import ActivityLog
from .middleware import get_current_user


@receiver(post_save)
def log_save(sender, instance, created, **kwargs):
    # Only log models from this app
    if sender._meta.app_label != 'ordenes':
        return
    # Avoid logging ActivityLog to prevent recursion
    if sender.__name__ == 'ActivityLog':
        return
    user = get_current_user()
    action = 'create' if created else 'update'
    ActivityLog.objects.create(
        user=user,
        action=action,
        model=sender.__name__,
        object_id=str(getattr(instance, 'pk', '')),
        message=str(instance),
    )


@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if sender._meta.app_label != 'ordenes':
        return
    user = get_current_user()
    ActivityLog.objects.create(
        user=user,
        action='delete',
        model=sender.__name__,
        object_id=str(getattr(instance, 'pk', '')),
        message=str(instance),
    )
