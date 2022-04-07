from django import template
from django.template.defaultfilters import stringfilter
import os

register = template.Library()

@stringfilter
def modify_filename(value):
    value = os.path.basename(os.path.normpath(value))
    return value

register.filter('modify_filename', modify_filename)