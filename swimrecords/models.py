from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_stroke(value):
    accepted_values = ['front crawl', 'butterfly', 'breast', 'back', 'freestyle']
    if value not in accepted_values:
        raise ValidationError(f"{value} is not a valid stroke")

def validate_distance(value):
    if int(value) < 50:
        raise ValidationError("Ensure this value is greater than or equal to 50.") 

def validate_record_date(value):
    if value > timezone.now():
        raise ValidationError("Can't set record in the future.")

class SwimRecord(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=30)
    team_name = models.CharField(max_length=20)
    relay = models.BooleanField()
    stroke = models.CharField(max_length=11, validators=[validate_stroke])
    distance = models.IntegerField(validators=[validate_distance])
    record_date = models.DateTimeField(validators=[validate_record_date])
    record_broken_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.record_broken_date > self.record_date:
            raise ValidationError("Can't break record before record was set.")
        super().save(*args, **kwargs)
