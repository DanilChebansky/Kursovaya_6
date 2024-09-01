from django import template

register = template.Library()


@register.simple_tag()
def mymedia(data):
    if data:
        return f'/media/{data}'
    return '#'
