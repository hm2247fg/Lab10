"""
ASGI config for wishlist project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Set the DJANGO_SETTINGS_MODULE environment variable to 'wishlist.settings'
# This specifies the settings file for the Django application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wishlist.settings')

# Get the ASGI application for the Django project
application = get_asgi_application()
