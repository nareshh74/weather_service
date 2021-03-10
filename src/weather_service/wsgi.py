"""
WSGI config for weather_service project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from weather_app.domain.weather_repository import weather_repository
import schedule


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_service.settings')

application = get_wsgi_application()

import time
import schedule
import threading


def run_continuously(interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


schedule.every(15).seconds.do(weather_repository.sync)

# Start the background thread
stop_run_continuously = run_continuously()
