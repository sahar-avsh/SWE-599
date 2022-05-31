from django import template
import os

register = template.Library()

@register.simple_tag
def get_env_var(key):
    return os.environ.get(key)

register.filter('get_env_var', get_env_var)