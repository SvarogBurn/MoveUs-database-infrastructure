from django.db import models


class Location(models.Model):
    """
    Static location data (country, city, postal code).
    Used as fallback when user doesn't enable location tracking.
    """
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = "location"
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        unique_together = [["country", "city", "postal_code"]]

    def __str__(self):
        if self.postal_code:
            return f"{self.city}, {self.country} ({self.postal_code})"
        return f"{self.city}, {self.country}"