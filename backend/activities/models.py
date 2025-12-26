from django.db import models


class Activity(models.Model):
    """
    Minimalna verzija aktivnosti.
    Enum logika može doći kasnije (Phase 2).
    """
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name
