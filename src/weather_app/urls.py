from django.urls import path, include
from weather_app import views


urlpatterns = [
    path('', views.WeatherAPI.as_view(), name='get weather info'),
    path('sendEmail', views.EmailAPI.as_view(), name='email weather info'),
    path('sync', views.manual_sync)
]
