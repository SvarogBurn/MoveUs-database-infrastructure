from django.db import models


class Gender(models.TextChoices):
    MALE = "M", "Male"
    FEMALE = "F", "Female"
    PREFER_NOT_TO_SAY = "PNS", "Prefer Not to Say"
    OTHER = "O", "Other"


class IndoorOutdoorPreference(models.TextChoices):
    INDOOR = "IN", "Indoor"
    OUTDOOR = "OUT", "Outdoor"
    NO_PREFERENCE = "NO", "No Preference"


class ActivityProficiency(models.TextChoices):
    BEGINNER = "BEG", "Beginner"
    INTERMEDIATE = "INT", "Intermediate"
    ADVANCED = "ADV", "Advanced"
    COMPETITIVE = "COMP", "Competitive"


class EventRating(models.IntegerChoices):
    ONE_STAR = 1, "1 Star"
    TWO_STARS = 2, "2 Stars"
    THREE_STARS = 3, "3 Stars"
    FOUR_STARS = 4, "4 Stars"
    FIVE_STARS = 5, "5 Stars"


class InteractionType(models.TextChoices):
    LIKE = "LIKE", "Like"
    NEUTRAL = "NEUTRAL", "Neutral"
    DISLIKE = "DISLIKE", "Dislike"