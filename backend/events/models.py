from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.enums import Gender, ActivityProficiency, EventRating, InteractionType
from users.models import User
from locations.models import Location
from activities.models import Activity


class Event(models.Model):
    """
    Represents a fitness/activity event that users can create and join.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_events"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Location information
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events"
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    address = models.CharField(max_length=300, blank=True)

    # Related activity
    activity = models.ForeignKey(
        Activity,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events"
    )

    class Meta:
        db_table = "event"
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ["-start_datetime"]

    def __str__(self):
        return f"{self.title} - {self.start_datetime.strftime('%Y-%m-%d %H:%M')}"


class EventRequirements(models.Model):
    """
    Defines requirements for event participation (gender, age, proficiency).
    """
    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="requirements"
    )
    gender = models.CharField(
        max_length=3,
        choices=Gender.choices,
        blank=True,
        null=True,
        help_text="Required gender for event participation (optional)"
    )
    min_age = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(120)],
        help_text="Minimum age for participation"
    )
    max_age = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(120)],
        help_text="Maximum age for participation"
    )
    required_proficiency = models.CharField(
        max_length=4,
        choices=ActivityProficiency.choices,
        blank=True,
        null=True,
        help_text="Minimum required proficiency level"
    )

    class Meta:
        db_table = "event_requirements"
        verbose_name = "Event Requirements"
        verbose_name_plural = "Event Requirements"

    def __str__(self):
        return f"Requirements for {self.event.title}"


class EventParticipation(models.Model):
    """
    Tracks user participation in events with optional rating and feedback.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="event_participations"
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="participations"
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    
    # Optional rating after event completion
    rating = models.IntegerField(
        choices=EventRating.choices,
        null=True,
        blank=True,
        help_text="User's rating of the event (1-5 stars)"
    )
    
    # Optional feedback text
    feedback = models.TextField(
        blank=True,
        help_text="Optional text feedback about the event"
    )

    class Meta:
        db_table = "event_participation"
        verbose_name = "Event Participation"
        verbose_name_plural = "Event Participations"
        unique_together = [["user", "event"]]
        ordering = ["-joined_at"]

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


class UserInteraction(models.Model):
    """
    Tracks user-to-user interactions during events.
    Defaults to NEUTRAL if no feedback is provided.
    """
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="interactions_given"
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="interactions_received"
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="user_interactions"
    )
    interaction_value = models.CharField(
        max_length=7,
        choices=InteractionType.choices,
        default=InteractionType.NEUTRAL,
        help_text="Like/Neutral/Dislike - defaults to Neutral if not specified"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_interaction"
        verbose_name = "User Interaction"
        verbose_name_plural = "User Interactions"
        unique_together = [["from_user", "to_user", "event"]]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.from_user.username} → {self.to_user.username} ({self.get_interaction_value_display()}) @ {self.event.title}"