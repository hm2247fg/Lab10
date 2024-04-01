from django.contrib import admin
from .models import Place

# This registers the Place model with the Django admin site,
# allowing you to manage Place objects through the admin interface
admin.site.register(Place)
