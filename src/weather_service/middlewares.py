# IMPORTS
from django.http import JsonResponse


# MIDDLEWARE DEFINITIONS
class ExceptionHandlerMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        try:
            return self.get_response(request)
        except Exception as e:
            return JsonResponse({"detail": "server error"}, status=500)
