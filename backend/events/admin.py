from django.contrib import admin
from .models import Event, EventParticipant, EventUserInteraction


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "activity", "location", "created_by", "start_time")
    search_fields = ("title",)
    fields = (
        "title",
        "description",
        "activity",
        "location",
        "start_time",
        "end_time",
        "created_by",
        "max_participants",
        "min_age",
        "max_age",
        "required_gender",
        "required_proficiency",
    )


@admin.register(EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ("user", "event", "joined_at")


@admin.register(EventUserInteraction)
class EventUserInteractionAdmin(admin.ModelAdmin):
    list_display = (
        "from_user",
        "to_user",
        "event",
        "interaction_value",
        "created_at",
    )
