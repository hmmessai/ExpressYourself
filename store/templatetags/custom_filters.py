from django import template

register = template.Library()

@register.filter
def to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return value
    
@register.filter
def excerpt(full_description):
    return f"{full_description[:20]}....."