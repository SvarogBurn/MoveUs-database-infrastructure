from django.db import models


class Location(models.Model):
    continent = models.CharField(max_length=32)
    country = models.CharField(max_length=64)
    city = models.CharField(max_length=64)

    postal_code = models.CharField(max_length=16, blank=True)

    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        indexes = [
            models.Index(fields=["continent", "country"]),
            models.Index(fields=["city"]),
            models.Index(fields=["latitude", "longitude"]),
        ]

    def __str__(self):
        return f"{self.city}, {self.country}"
