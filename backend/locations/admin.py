from django.contrib import admin
from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["city", "country", "postal_code"]
    list_filter = ["country"]
    search_fields = ["city", "country", "postal_code"]
    ordering = ["country", "city"]