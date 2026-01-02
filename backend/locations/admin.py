from django.contrib import admin
from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("continent", "country", "city", "postal_code")
    search_fields = ("city", "country", "postal_code")
