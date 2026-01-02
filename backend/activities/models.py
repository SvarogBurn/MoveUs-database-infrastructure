from django.db import models


class Activity(models.Model):
    name = models.CharField(max_length=64, unique=True)

    metabolic_demand = models.FloatField()
    neurocognitive_precision = models.FloatField()
    risk_modulation = models.FloatField()
    kinesthetic_intelligence = models.FloatField()
    environmental_dependency = models.FloatField()
    collaborative_dynamics = models.FloatField()

    def __str__(self):
        return self.name
