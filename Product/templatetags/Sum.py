from django import template
register = template.Library()

@register.filter
def Sum(a,b):
    if not b:
        return a+0
    return a+len(b)-1