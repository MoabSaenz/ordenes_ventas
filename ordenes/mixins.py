from django.db import models
from django.utils import timezone
from .middleware import get_current_user


class AuditMixin(models.Model):
    """Adds created/updated timestamps and user attribution where possible."""

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'auth.User', null=True, blank=True, related_name='+', on_delete=models.SET_NULL
    )
    updated_by = models.ForeignKey(
        'auth.User', null=True, blank=True, related_name='+', on_delete=models.SET_NULL
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not self.pk and not getattr(self, 'created_by', None):
            try:
                self.created_by = user
            except Exception:
                pass
        if user:
            try:
                self.updated_by = user
            except Exception:
                pass
        super().save(*args, **kwargs)
