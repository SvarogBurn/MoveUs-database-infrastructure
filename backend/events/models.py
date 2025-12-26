from django.db import models
from django.conf import settings
from activities.models import Activity


User = settings.AUTH_USER_MODEL


class Event(models.Model):
    """
    Minimalni event za Phase 1.
    """
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    location = models.CharField(max_length=128)

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    max_participants = models.PositiveIntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def participant_count(self):
        return self.members.filter(participates=True).count()

    def __str__(self):
        return self.title

class EventMember(models.Model):
    """
    Povezuje usera i event.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="members")

    participates = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "event")

    def __str__(self):
        return f"{self.user} -> {self.event}"
