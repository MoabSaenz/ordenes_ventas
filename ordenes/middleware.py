import threading

_thread_locals = threading.local()


def get_current_user():
    return getattr(_thread_locals, 'user', None)


class CurrentUserMiddleware:
    """Middleware that stores the current user in thread-local storage.

    Signals and other background logic can call `get_current_user()` to
    attribute actions to the active request user when available.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.user = getattr(request, 'user', None)
        response = self.get_response(request)
        return response
