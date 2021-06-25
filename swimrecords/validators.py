from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_date(value):
    # if the date_time is greater than now
    if value > timezone.now():
        # raise ValidationError()
        raise ValidationError("Can't set record in the future.")
