from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.enums import Gender, IndoorOutdoorPreference, ActivityProficiency
from locations.models import Location
from activities.models import Activity


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser
    Includes additional fields for fitness/activity preferences
    """
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=3,
        choices=Gender.choices,
        blank=True,
        null=True
    )
    home_city = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        help_text="Fallback location if user doesn't enable location tracking"
    )
    indoor_outdoor_preference = models.CharField(
        max_length=3,
        choices=IndoorOutdoorPreference.choices,
        default=IndoorOutdoorPreference.NO_PREFERENCE
    )
    frequency_of_physical_activity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="How many times per month user exercises"
    )
    desired_frequency_of_physical_activity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="How many times per month user wants to exercise"
    )

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"
        indexes = [
            models.Index(fields=['home_city']),
        ]

    def __str__(self):
        return self.username


# REMOVED: UserLocation model
# User real-time location is now stored in Redis instead of PostgreSQL
# This is more efficient for high-frequency updates and doesn't fill up the database
# See utils/location_cache.py for Redis-based location tracking


class PsychologicalProfile(models.Model):
    """
    Stores OCEAN (Big Five) personality traits for each user
    All traits are normalized between 0 and 1
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="psychological_profile"
    )
    openness = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Openness to experience [0-1]"
    )
    conscientiousness = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Conscientiousness [0-1]"
    )
    extraversion = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Extraversion [0-1]"
    )
    agreeableness = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Agreeableness [0-1]"
    )
    neuroticism = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Neuroticism [0-1]"
    )

    class Meta:
        db_table = "psychological_profile"
        verbose_name = "Psychological Profile"
        verbose_name_plural = "Psychological Profiles"

    def __str__(self):
        return f"Psychological Profile - {self.user.username}"


class UserActivityProficiency(models.Model):
    """
    Tracks user's proficiency level for different activities
    Many-to-many relationship between User and Activity with proficiency level
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="activity_proficiencies"
    )
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name="user_proficiencies"
    )
    proficiency_level = models.CharField(
        max_length=4,
        choices=ActivityProficiency.choices,
        default=ActivityProficiency.BEGINNER
    )

    class Meta:
        db_table = "user_activity_proficiency"
        verbose_name = "User Activity Proficiency"
        verbose_name_plural = "User Activity Proficiencies"
        unique_together = [["user", "activity"]]
        indexes = [
            models.Index(fields=['user', 'activity']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.activity.name} ({self.get_proficiency_level_display()})"