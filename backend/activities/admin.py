from django.contrib import admin
from .models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "metabolic_demand",
        "neurocognitive_precision",
        "risk_modulation",
        "kinesthetic_intelligence",
        "environmental_dependency",
        "collaborative_dynamics",
    ]
    search_fields = ["name"]
    ordering = ["name"]
    
    fieldsets = (
        ("Basic Information", {
            "fields": ("name",)
        }),
        ("Activity Metrics", {
            "fields": (
                "metabolic_demand",
                "neurocognitive_precision",
                "risk_modulation",
                "kinesthetic_intelligence",
                "environmental_dependency",
                "collaborative_dynamics",
            )
        }),
    )