from django import template

register = template.Library()

def get_access_level(value, arg):
    return value.has_what_access(arg)

register.filter('get_access_level', get_access_level)