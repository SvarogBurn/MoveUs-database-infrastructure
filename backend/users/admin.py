from django.contrib import admin
from .models import User, UserActivity, PsychologicalProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "gender", "physical_activity_frequency")
    search_fields = ("username", "email")
    fields = (
        "username",
        "email",
        "password",
        "date_of_birth",
        "gender",
        "location",
        "height_cm",
        "weight_kg",
        "budget_eur",
        "physical_activity_frequency",
        "desired_physical_activity_frequency",
        "is_professional",
        "social_importance",
        "indoor_outdoor_preference",
        "preferred_event_duration_minutes",
    )


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ("user", "activity", "proficiency_level")


@admin.register(PsychologicalProfile)
class PsychologicalProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "openness", "extraversion")
