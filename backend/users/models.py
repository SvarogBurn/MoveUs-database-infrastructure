# users/models.py
import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=32, unique=True)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    date_of_birth = models.DateField(null=True, blank=True)

    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)

    preferred_activities = models.ManyToManyField(
        "activities.Activity",
        blank=True,
        related_name="preferred_by_users"
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    @property
    def age(self):
        if not self.date_of_birth:
            return None
        return (datetime.date.today() - self.date_of_birth).days // 365

    def __str__(self):
        return self.email
