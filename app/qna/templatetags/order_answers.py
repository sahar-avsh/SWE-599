from django import template

register = template.Library()

def order_answers(value):
    return sorted(value, key=lambda x: x.get_vote_score(), reverse=True)

register.filter('order_answers', order_answers)