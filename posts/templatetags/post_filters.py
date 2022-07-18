from django import template

register = template.Library()


@register.filter(name='count_comments')
def count_comments(amount):
    if amount == 0:
        return 'No comments'
    elif amount > 1:
        return f'{amount} comments'
    else:
        return f'{amount} comment'
