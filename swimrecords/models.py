from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

def validate_length(field_value):
    if len(field_value) < 1:
        raise ValidationError('This field cannot be blank.')

def validate_boolean(field_value):
    if field_value != True | field_value != False:
        raise ValidationError('"None" value must be either True or False.')

def validate_stroke(field_value):
    valid_strokes = ['front crawl', 'butterfly', 'breast', 'back', 'freestyle']
    if field_value not in valid_strokes:
        raise ValidationError(
            _('%(field_value)s is not a valid stroke.'),
            params={'field_value': field_value},
        )

def validate_distance(field_value):
    if field_value < 50:
        raise ValidationError('Ensure this value is greater than or equal to 50.')

def validate_future_records(field_value):
    if field_value > timezone.now():
        raise ValidationError("Can't set record in the future.")

def validate_break_set_record(field_value):
    if field_value < timezone.now():
        raise ValidationError("Can't break record before record was set.")


class SwimRecord(models.Model):
    first_name = models.CharField(max_length = 25, validators=[validate_length])
    last_name = models.CharField(max_length = 25, validators=[validate_length])
    team_name = models.CharField(max_length = 35, validators=[validate_length])
    relay = models.BooleanField(default=False, validators=[validate_boolean])
    stroke = models.CharField(max_length = 15, validators=[validate_stroke])
    distance = models.IntegerField(validators=[validate_distance])
    record_date = models.DateTimeField(validators=[validate_future_records])
    record_broken_date = models.DateTimeField(validators=[validate_break_set_record])
