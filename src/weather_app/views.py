from django.http import JsonResponse
from weather_app.domain.email_service import EmailService
from weather_app.domain.weather_repository import weather_repository
import json
from rest_framework.views import APIView 
from authentication.permissions import IsLoggedIn


# Create your views here.
class WeatherAPI(APIView):
    permission_classes = (IsLoggedIn, ) 

    def get(self, request):
        return get_weather_info(request._request)

class EmailAPI(APIView):
    permission_classes = (IsLoggedIn, ) 

    def get(self, request):
        return email_weather_info(request._request)

def get_weather_info(request):
    start_index = int(request.GET.get("start", 0))
    end_index = int(request.GET.get("end", start_index + 10))
    data = weather_repository.query(start_index, end_index)
    city_count = weather_repository.get_city_count()
    return JsonResponse({"data": data, "totalCityCount": city_count}, status=200)

def email_weather_info(request):
    try:
        body = json.loads(request.body)
        receiver_email_list = body["receiverEmailList"]
    except Exception as e:
        return JsonResponse({"detail": "receipient email list/missing or invalid"}, status=400)
    email_service = EmailService()
    excel_file = weather_repository.get_data_as_excel()
    email_service.send_email(receiver_email_list, attachment_file=excel_file)
    return JsonResponse({"detail": "success"}, status=200)

def manual_sync(_):
    weather_repository.sync()
    return JsonResponse({"detail": "success"}, status=200)
