from django.contrib import admin
from .models import User, UserLocation, PsychologicalProfile, UserActivityProficiency


class UserLocationInline(admin.StackedInline):
    model = UserLocation
    can_delete = False
    verbose_name_plural = "Current Location"
    extra = 0


class PsychologicalProfileInline(admin.StackedInline):
    model = PsychologicalProfile
    can_delete = False
    verbose_name_plural = "Psychological Profile"
    extra = 0


class UserActivityProficiencyInline(admin.TabularInline):
    model = UserActivityProficiency
    extra = 1
    verbose_name = "Activity Proficiency"
    verbose_name_plural = "Activity Proficiencies"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [UserLocationInline, PsychologicalProfileInline, UserActivityProficiencyInline]
    
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "date_of_birth",
        "gender",
        "date_joined"
    ]
    
    list_filter = ["gender", "indoor_outdoor_preference", "date_joined"]
    
    search_fields = ["username", "email", "first_name", "last_name"]
    
    readonly_fields = ["date_joined", "last_login"]
    
    fieldsets = (
        ("Account Information", {
            "fields": ("username", "password", "email", "date_joined", "last_login")
        }),
        ("Personal Information", {
            "fields": ("first_name", "last_name", "date_of_birth", "gender", "home_city")
        }),
        ("Activity Preferences", {
            "fields": (
                "indoor_outdoor_preference",
                "frequency_of_physical_activity",
                "desired_frequency_of_physical_activity"
            )
        }),
    )
    
    add_fieldsets = (
        ("Account Information", {
            "fields": ("username", "password1", "password2", "email")
        }),
        ("Personal Information", {
            "fields": ("first_name", "last_name", "date_of_birth", "gender", "home_city")
        }),
        ("Activity Preferences", {
            "fields": (
                "indoor_outdoor_preference",
                "frequency_of_physical_activity",
                "desired_frequency_of_physical_activity"
            )
        }),
    )


@admin.register(UserLocation)
class UserLocationAdmin(admin.ModelAdmin):
    list_display = ["user", "latitude", "longitude", "updated_at"]
    search_fields = ["user__username"]
    readonly_fields = ["updated_at"]


@admin.register(PsychologicalProfile)
class PsychologicalProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "openness",
        "conscientiousness",
        "extraversion",
        "agreeableness",
        "neuroticism"
    ]
    search_fields = ["user__username"]
    
    fieldsets = (
        ("User", {
            "fields": ("user",)
        }),
        ("OCEAN Personality Traits", {
            "fields": (
                "openness",
                "conscientiousness",
                "extraversion",
                "agreeableness",
                "neuroticism"
            )
        }),
    )


@admin.register(UserActivityProficiency)
class UserActivityProficiencyAdmin(admin.ModelAdmin):
    list_display = ["user", "activity", "proficiency_level"]
    list_filter = ["proficiency_level", "activity"]
    search_fields = ["user__username", "activity__name"]
    ordering = ["user", "activity"]