from django import template
from django.utils import timezone


MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR

register = template.Library()


@register.filter
def model_type(value):
    return type(value).__name__


@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    if user == context['user']:
        return 'you'
    return user.username


@register.filter
def get_posted_at_display(posted_at):
    seconds_ago = (timezone.now()-posted_at).total_seconds()
    if seconds_ago <= HOUR:
        if int(seconds_ago // MINUTE) < 2:  # I just wrote this logic to work around the grammar. I can extend it to
            # now if its less than 1 minute
            return f'Posted {int(seconds_ago // MINUTE)} minute ago.'
        else:
            return f'Posted {int(seconds_ago // MINUTE)} minutes ago.'
    elif seconds_ago <= DAY:
        return f'Posted {int(seconds_ago // HOUR)} hours ago.'
    return f'Posted at {posted_at.strftime("%H:%M %d %b %y")}'
