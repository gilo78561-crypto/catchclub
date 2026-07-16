from django import template
from social.mentions import rendre_mentions

register = template.Library()


@register.filter(name='mentions')
def mentions(texte):
    return rendre_mentions(texte)
