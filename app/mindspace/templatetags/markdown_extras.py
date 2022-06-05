from django import template
from django.template.defaultfilters import stringfilter

import markdown as md

register = template.Library()

@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])

register.filter('markdown', markdown)