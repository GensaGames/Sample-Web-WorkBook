from django import template
from datetime import date, timedelta

register = template.Library()


# Using just for changing orientation LEFT - RIGHT
@register.filter(name='get_due_date_string')
def get_due_date_string(value):
    return value % 2 == 0