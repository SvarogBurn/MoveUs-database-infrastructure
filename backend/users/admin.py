from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "first_name", "last_name", "gender")
    fields = (
        "email",
        "username",
        "first_name",
        "last_name",
        "date_of_birth",
        "gender",
        "preferred_activities",
        "password",
    )
