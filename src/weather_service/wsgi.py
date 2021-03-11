"""
WSGI config for weather_service project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from weather_service.startup import start_app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_service.settings')

application = get_wsgi_application()

start_app()
