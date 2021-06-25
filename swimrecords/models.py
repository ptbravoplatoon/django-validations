from django.db import models
from django.core.validators import MaxValueValidator, MinLengthValidator, MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

class SwimRecord(models.Model):
    first_name = models.CharField(max_length = 30, validators = [MinLengthValidator(1)])
    last_name = models.CharField(max_length = 30, validators = [MinLengthValidator(1)])
    team_name = models.CharField(max_length = 30, validators = [MinLengthValidator(1)])
    relay = models.BooleanField(blank = False)

    STROKE_CHOICES = [
        ('front crawl', 'front crawl'), 
        ('butterfly', 'butterfly'), 
        ('breast', 'breast'), 
        ('back', 'back'), 
        ('freestyle', 'freestyle')
    ]
    stroke = models.CharField(max_length = 30, choices = STROKE_CHOICES)

    distance = models.IntegerField(validators = [MinValueValidator(50)])

    def no_future_dates(value):
        if value > timezone.now():
            raise ValidationError("Can't set record in the future.")
        return value
    record_date = models.DateTimeField(validators = [no_future_dates])

    # def save(self, *args, **kwargs):
    #     if self.record_broken_date < self.record_date:
    #         raise ValidationError("Can't break record before record was set.")
    #     super(SwimRecord, self).save(*args, **kwargs)


    # def no_future_record_breaks(self):
    #     if self.record_broken_date < self.record_date:
    #         raise ValidationError("Can't break record before record was set.")
    #     pass
    # record_broken_date = models.DateTimeField(validators = [no_future_record_breaks])

    # def full_clean(self, *args, **kwargs):
    #     if self.record_broken_date < self.record_date:
    #         raise ValidationError("Can't break record before record was set.")
    #     super(SwimRecord, self).full_clean(*args, **kwargs)
    record_broken_date = models.DateTimeField()

