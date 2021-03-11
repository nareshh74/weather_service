from weather_app.domain.weather_repository import weather_repository
import schedule
import time
import schedule
import threading
import os
from django.conf import settings


def start_app():

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


    schedule.every(30).minutes.do(weather_repository.sync)

    # Start the background thread
    stop_run_continuously = run_continuously()
