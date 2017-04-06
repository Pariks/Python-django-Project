from django import template

register = template.Library()

@register.inclusion_tag('tags/poster.html')
def poster(event):
    return {'event': event}
