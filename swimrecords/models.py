from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator
from swimrecords.validators import validate_date


class SwimRecord(models.Model):
    STROKE_CHOICES = [
        ("front crawl", "front crawl"),
        ("butterfly", "butterfly"),
        ("breast", "breast"),
        ("back", "back"),
        ("freestyle", "freestyle"),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    team_name = models.CharField(max_length=100)
    # relay = models.BooleanField(default=False) ... not sure why this doesnt pass https://docs.djangoproject.com/en/3.2/ref/models/fields/#binaryfield
    relay = models.BooleanField()
    stroke = models.CharField(max_length=11, choices=STROKE_CHOICES)
    distance = models.IntegerField(validators=[MinValueValidator(50)])
    record_date = models.DateTimeField(validators=[validate_date])
    record_broken_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.record_broken_date > self.record_date:
            raise ValidationError("Can't break record before record was set.")
        super().save(*args, **kwargs)
