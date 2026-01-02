from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Event(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    location = models.ForeignKey(
        "locations.Location",
        on_delete=models.CASCADE
    )

    activity = models.ForeignKey(
        "activities.Activity",
        on_delete=models.CASCADE
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_events"
    )

    participants = models.ManyToManyField(
        User,
        through="EventParticipant",
        related_name="joined_events"
    )

    max_participants = models.PositiveIntegerField(null=True, blank=True)

    min_age = models.PositiveSmallIntegerField(null=True, blank=True)
    max_age = models.PositiveSmallIntegerField(null=True, blank=True)

    required_gender = models.CharField(
        max_length=1,
        choices=[("M", "Male"), ("F", "Female"), ("O", "Other")],
        null=True,
        blank=True
    )

    required_proficiency = models.CharField(
        max_length=16,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["start_time"]),
            models.Index(fields=["activity", "start_time"]),
            models.Index(fields=["created_by"]),
        ]
        ordering = ["-start_time"]

    def __str__(self):
        return self.title

class EventParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    joined_at = models.DateTimeField(auto_now_add=True)

    event_rating = models.PositiveSmallIntegerField(null=True, blank=True)
    organizer_rating = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "event")
        indexes = [
            models.Index(fields=["joined_at"]),
        ]

    def __str__(self):
        return f"{self.user} @ {self.event}"
