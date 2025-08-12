"""
WSGI config for mabuhaypowers_pom project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from monitoring.apps import start_status_update_thread

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mabuhaypowers_pom.settings')

application = get_wsgi_application()

start_status_update_thread()
