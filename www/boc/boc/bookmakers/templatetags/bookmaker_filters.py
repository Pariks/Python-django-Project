from django import template
from bookmakers.models import Banner

register = template.Library()

@register.inclusion_tag('tags/banner_wide.html')
def wide_banner():
    banner_desktop = Banner.get_random_banner(size='WI',platform='DE')
    banner_mobile = Banner.get_random_banner(size='WI',platform='MO')
    return {'banner_desktop': banner_desktop, 'banner_mobile': banner_mobile}

@register.inclusion_tag('tags/banner_tall.html')
def tall_banner():
    banner_desktop = Banner.get_random_banner(size='TA',platform='DE')
    return {'banner_desktop': banner_desktop}

@register.inclusion_tag('tags/banner_square.html')
def square_banner():
    banner_desktop = Banner.get_random_banner(size='SQ',platform='DE')
    return {'banner_desktop': banner_desktop}