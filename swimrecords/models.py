from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime
from django.utils import timezone

class SwimRecord(models.Model):
    first_name = models.CharField()
    first_name.max_length = 20
    last_name = models.CharField()
    last_name.max_length = 20
    team_name = models.CharField()
    team_name.max_length = 20
    relay = models.BooleanField()
    stroke = models.CharField()
    stroke.max_length = 20
    distance = models.IntegerField()
    record_date = models.DateTimeField()
    record_broken_date = models.DateTimeField()

    def full_clean(self):
        valid_strokes = ['freestyle', 'butterly', 'breaststroke', 'backstroke']
        errors = {
            "first_name":[],
            "last_name":[],
            "team_name":[],
            "relay":[],
            "stroke":[],
            "distance":[],
            "record_date":[],
            "record_broken_date":[]
        }
        if len(self.first_name) == 0:
            errors["first_name"].append("This field cannot be blank.")
        if len(self.last_name) == 0:
            errors["last_name"].append("This field cannot be blank.")
        if len(self.team_name) == 0:
            errors["team_name"].append("This field cannot be blank.")
        if self.relay == None:
            errors["relay"].append("'None' value must be either True or False.")
        if self.stroke not in valid_strokes:
            errors["stroke"].append(f"{self.stroke} is not a valid stroke.")
        if self.distance == None or self.distance < 50:
            errors["distance"].append("Ensure this value is greater than or equal to 50.")
        if (self.record_date != None and self.record_broken_date != None):
            if self.record_broken_date < self.record_date:
                errors["record_broken_date"].append("Can't break record before record was set.")
        if self.record_date != None:
            if self.record_date > timezone.now():
                errors["record_date"].append("Can't set record in the future.")

        for key in errors.keys():
            if len(errors[key]) > 0:
                raise ValidationError(errors)
        return super().full_clean()