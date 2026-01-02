import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=32, unique=True)

    date_of_birth = models.DateField()

    gender = models.CharField(
        max_length=1,
        choices=[("M", "Male"), ("F", "Female"), ("O", "Other")],
        null=True,
        blank=True
    )

    location = models.ForeignKey(
        "locations.Location",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    height_cm = models.PositiveSmallIntegerField(null=True, blank=True)
    weight_kg = models.PositiveSmallIntegerField(null=True, blank=True)

    budget_eur = models.PositiveIntegerField(null=True, blank=True)

    physical_activity_frequency = models.PositiveSmallIntegerField(
        help_text="Current activities per month",
        default=0
    )

    desired_physical_activity_frequency = models.PositiveSmallIntegerField(
        help_text="Desired activities per month",
        default=0
    )

    is_professional = models.BooleanField(default=False)

    social_importance = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        default=3
    )

    indoor_outdoor_preference = models.CharField(
        max_length=16,
        choices=[
            ("indoor", "Indoor"),
            ("outdoor", "Outdoor"),
            ("none", "No preference"),
        ],
        default="none"
    )

    preferred_event_duration_minutes = models.PositiveIntegerField(
        null=True, blank=True
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    @property
    def age(self):
        today = datetime.date.today()
        return (today - self.date_of_birth).days // 365

    def __str__(self):
        return self.username


class UserActivity(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="activities"
    )
    activity = models.ForeignKey(
        "activities.Activity",
        on_delete=models.CASCADE
    )

    proficiency_level = models.CharField(
        max_length=16,
        choices=[
            ("beginner", "Beginner"),
            ("intermediate", "Intermediate"),
            ("advanced", "Advanced"),
            ("competitive", "Competitive"),
        ]
    )

    class Meta:
        unique_together = ("user", "activity")

    def __str__(self):
        return f"{self.user} – {self.activity} ({self.proficiency_level})"


class PsychologicalProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )

    openness = models.FloatField()
    conscientiousness = models.FloatField()
    extraversion = models.FloatField()
    agreeableness = models.FloatField()
    neuroticism = models.FloatField()

    def __str__(self):
        return f"Psych profile for {self.user}"
