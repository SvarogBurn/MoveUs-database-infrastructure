import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Minimalni MoveUs user za Phase 1.
    """
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(unique=True)

    date_of_birth = models.DateField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def save(self, *args, **kwargs):
        if self.username:
            self.username = self.username.lower()
        super().save(*args, **kwargs)

    @property
    def age(self):
        if not self.date_of_birth:
            return None
        return (datetime.date.today() - self.date_of_birth).days // 365

    def __str__(self):
        return self.email
