from django.contrib import admin
from .models import Event, EventRequirements, EventParticipation, UserInteraction


class EventRequirementsInline(admin.StackedInline):
    model = EventRequirements
    can_delete = False
    verbose_name_plural = "Event Requirements"
    extra = 0


class EventParticipationInline(admin.TabularInline):
    model = EventParticipation
    extra = 0
    readonly_fields = ["joined_at"]
    fields = ["user", "joined_at", "rating", "feedback"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [EventRequirementsInline, EventParticipationInline]
    
    list_display = [
        "title",
        "start_datetime",
        "end_datetime",
        "created_by",
        "location",
        "activity",
        "created_at"
    ]
    list_filter = ["start_datetime", "activity", "location"]
    search_fields = ["title", "description", "created_by__username"]
    readonly_fields = ["created_at"]
    date_hierarchy = "start_datetime"
    
    fieldsets = (
        ("Basic Information", {
            "fields": ("title", "description", "activity", "created_by")
        }),
        ("Date & Time", {
            "fields": ("start_datetime", "end_datetime", "created_at")
        }),
        ("Location Details", {
            "fields": ("location", "latitude", "longitude", "address")
        }),
    )


@admin.register(EventRequirements)
class EventRequirementsAdmin(admin.ModelAdmin):
    list_display = ["event", "gender", "min_age", "max_age", "required_proficiency"]
    list_filter = ["gender", "required_proficiency"]
    search_fields = ["event__title"]


@admin.register(EventParticipation)
class EventParticipationAdmin(admin.ModelAdmin):
    list_display = ["user", "event", "joined_at", "rating"]
    list_filter = ["rating", "joined_at"]
    search_fields = ["user__username", "event__title"]
    readonly_fields = ["joined_at"]
    ordering = ["-joined_at"]
    
    fieldsets = (
        ("Participation Info", {
            "fields": ("user", "event", "joined_at")
        }),
        ("Feedback", {
            "fields": ("rating", "feedback")
        }),
    )


@admin.register(UserInteraction)
class UserInteractionAdmin(admin.ModelAdmin):
    list_display = ["from_user", "to_user", "event", "interaction_value", "created_at"]
    list_filter = ["interaction_value", "created_at"]
    search_fields = ["from_user__username", "to_user__username", "event__title"]
    readonly_fields = ["created_at"]
    ordering = ["-created_at"]
    
    fieldsets = (
        ("Interaction Details", {
            "fields": ("from_user", "to_user", "event", "interaction_value")
        }),
        ("Metadata", {
            "fields": ("created_at",)
        }),
    )