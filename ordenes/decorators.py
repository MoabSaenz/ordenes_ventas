from functools import wraps
from django.core.exceptions import PermissionDenied


def has_permission(perm):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.has_perm(perm):
                raise PermissionDenied("No tienes permiso para realizar esta acción")
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator
