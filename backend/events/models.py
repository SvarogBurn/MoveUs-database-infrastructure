# events/models.py
from django.conf import settings
from django.db import models
from activities.models import Activity

User = settings.AUTH_USER_MODEL

class Event(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    location = models.CharField(max_length=128)

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

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

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        indexes = [
            models.Index(fields=['start_time']),  # Za filtriranje po vremenu
            models.Index(fields=['activity', 'start_time']),  # Composite za aktivnost+vrijeme
            models.Index(fields=['location']),  # Za prostorno pretraživanje
            models.Index(fields=['created_by']),
        ]
        ordering = ['-start_time']


class EventParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "event")
        indexes = [
            models.Index(fields=['joined_at']),  # Za sortiranje po vremenu pridruživanja
        ]
        
