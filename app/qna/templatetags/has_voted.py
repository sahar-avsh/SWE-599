from django import template
from qna.models import Activity

register = template.Library()

@register.simple_tag
def has_voted(value, arg):
    try:
        vote = Activity.objects.get(owner=arg, answer=value)
        return True
    except Activity.DoesNotExist:
        return False

register.filter('has_voted', has_voted)