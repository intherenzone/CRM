from django.contrib import admin

# Register your models here.
from organizations.models import Organization


admin.site.register(Organization)
