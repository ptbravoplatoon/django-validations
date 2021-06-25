from django.db import models 
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError



class SwimRecord(models.Model):
    # id = models.AutoField(primary_key=True)
    # pass
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    team_name = models.CharField(max_length=50, blank=False)
    relay = models.BooleanField(null=False)

    STROKE_CHOICES = (
        ("FRONT_CRAWL",'front crawl'),
        ("BUTTERFLY", 'butterfly'),
        ("BREAST", 'breast'),
        ("BACK", 'back'),
        ("FREESTYLE",'freestyle')
    )
    stroke = models.CharField(max_length=50, choices=STROKE_CHOICES)
    distance = models.IntegerField(validators=[MinValueValidator(50)])

    def validate_record_date(value):
        today = timezone.now()
        if value > today:
            raise ValidationError("Can't set record in the future.")
        else:
            return value
    record_date = models.DateTimeField(validators=[validate_record_date])
    
    def validate_record_broken_date(value):
        today = timezone.now()
        if value < today:
            raise ValidationError("Can't break record before record was set.")
        else:
            return value
    record_broken_date = models.DateTimeField(validators=[validate_record_broken_date])
