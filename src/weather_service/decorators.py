from functools import wraps
from django.http import JsonResponse


def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = args[0].user
        if not user.is_authenticated:
            return JsonResponse({"detail": "no user logged in"}, status=401)
        return f(*args, **kwargs)
    return decorated
