from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import *
from django.utils import timezone

def validate_stroke(stroke_type):
    stroke_list = ['front crawl', 'butterfly', 'breast','back',
    'freestyle']
    if stroke_type not in stroke_list:
        raise ValidationError(f'{stroke_type} is not a valid stroke')

def validate_broken_date(record_date,record_broken_date):
    if record_date > record_broken_date:
        raise ValidationError("Can't break record before record was.") 

def validate_record_date(give_date):
    if give_date > timezone.now():
        raise ValidationError("Can't set record in the future.")

class SwimRecord(models.Model):
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    team_name = models.CharField(max_length=255)
    #Needed to pass None test blank = true and null = true
    relay = models.BooleanField(blank=True, null=True)
    stroke = models.CharField(max_length=100, validators=[validate_stroke])
    
    distance = models.IntegerField(validators=[MinValueValidator(50)])
    record_date = models.DateTimeField(validators =[validate_record_date])
    record_broken_date = models.DateTimeField()
    
    
    # delete me when you start writing in validations
    # first_name = models.CharField()
    # last_name = models.CharField()
    # team_name = models.CharField()
    # relay = models.BooleanField()
    # stroke = models.CharField()
    # distance = models.IntegerField()
    # record_date = models.DateTimeField()
    # record_broken_date = models.DateTimeField()
    
    def full_clean(self):
        if self.record_broken_date and self.record_date:
            if self.record_broken_date < self.record_date:
                raise ValidationError({'record_broken_date': "Can't break record before record was set."})
