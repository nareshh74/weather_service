from django.http import JsonResponse
import json
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from authentication.permissions import IsLoggedIn
from authentication.serializers import LoginSerializer
from rest_framework_simplejwt.views import TokenViewBase


# Create your views here.
class LoginView(TokenViewBase):
    serializer_class = LoginSerializer


class LogoutAPI(APIView):
    permission_classes = (IsLoggedIn,)

    def post(self, request):
        settings.LOGOUT_USERS_SET.add(request.user.username)
        print(settings.LOGOUT_USERS_SET)
        return JsonResponse({"detail": "success"}, status=200)
