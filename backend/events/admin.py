from django.contrib import admin
from .models import Event, EventParticipant

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "activity", "location", "created_by", "start_time")
    fields = (
        "title",
        "description",
        "activity",
        "location",
        "start_time",
        "end_time",
        "created_by",
        "max_participants",
    )

admin.site.register(EventParticipant)
