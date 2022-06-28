import re
from django.core.exceptions import ValidationError


def total_length_of_text(value):
    string = re.sub("[\s\t\n]{2,}", " ")
    
    if len(string)<50:
        raise ValidationError("String is smaller than the expected length.")