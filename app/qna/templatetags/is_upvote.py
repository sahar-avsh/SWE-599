from django import template
from qna.models import Activity

register = template.Library()

@register.simple_tag
def is_upvote(value, arg):
    vote = Activity.objects.get(owner=arg, answer=value)
    return True if vote.activity_type == 'U' else False

register.filter('is_upvote', is_upvote)