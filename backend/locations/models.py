from django.contrib.gis.db import models as gis_models
from django.db import models


class Location(models.Model):
    """
    Static location data with PostGIS support for spatial queries
    """
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    
    # PostGIS PointField for spatial indexing
    # geography=True uses WGS84 and calculates distances in meters
    point = gis_models.PointField(geography=True, null=True, blank=True, srid=4326)

    class Meta:
        db_table = "location"
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        unique_together = [["country", "city", "postal_code"]]
        indexes = [
            gis_models.Index(fields=['point']),  # Spatial index (R-tree)
        ]

    def __str__(self):
        if self.postal_code:
            return f"{self.city}, {self.country} ({self.postal_code})"
        return f"{self.city}, {self.country}"