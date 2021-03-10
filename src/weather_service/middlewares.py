# IMPORTS
# 3rd party imports
from django.core import exceptions
from django.contrib.auth import authenticate, login
import json
from django.http import JsonResponse


# MIDDLEWARE DEFINITIONS
class AuthMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            username = body["username"]
            password = body["password"]
        except Exception as e:
            try:
                user = request.user
                if not user.is_authenticated:
                    raise
            except Exception as e:
                return JsonResponse({"detail": "no user logged in"}, status=401)
        return self.get_response(request)


class ExceptionHandlerMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        try:
            return self.get_response(request)
        except Exception as e:
            return JsonResponse({"detail": "server error"}, status=500)
