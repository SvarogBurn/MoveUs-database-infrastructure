from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Activity(models.Model):
    """
    Represents a physical or recreational activity with various metrics.
    All metrics are normalized between 0 and 1.
    """
    name = models.CharField(max_length=100, unique=True)
    
    metabolic_demand = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Normalized [0–1] physical energy expenditure",
    )
    neurocognitive_precision = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Normalized [0–1] cognitive complexity",
    )
    risk_modulation = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Normalized [0–1] injury / risk exposure",
    )
    kinesthetic_intelligence = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Normalized [0–1] motor coordination demand",
    )
    environmental_dependency = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Normalized [0–1] dependence on environment",
    )
    collaborative_dynamics = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Normalized [0–1] social/team dependence",
    )

    class Meta:
        db_table = "activity"
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
        ordering = ["name"]

    def __str__(self):
        return self.name