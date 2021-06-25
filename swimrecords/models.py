from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

def validate_stroke(value):
    if value not in ['front crawl', 'butterfly', 'breast', 'back', 'freestyle']:
        raise ValidationError(f"{value} is not a valid stroke")

def validate_record_date(value):
    if value > timezone.now():
        raise ValidationError("Can't set record in the future.")




class SwimRecord(models.Model):

    # def validate_record_broken_date(self, value):
    #     if value < self.record_date:
    #         raise ValidationError("Can't break record before record was set.")

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    team_name = models.CharField(max_length=50)
    relay = models.BooleanField()
    stroke = models.CharField(max_length=20, validators=[validate_stroke])
    distance = models.IntegerField(validators=[MinValueValidator(50)])
    record_date = models.DateTimeField(validators=[validate_record_date])
    record_broken_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.record_date < self.record_broken_date:
            raise ValidationError(_("Can't break record before record was set."), code='invalid')

        super(SwimRecord, self).save(*args, **kwargs)