from django import template
register = template.Library()

@register.filter
def imageYoutube(a):
    return a.replace("https://www.youtube.com/embed/","")