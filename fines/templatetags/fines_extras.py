from django import template

from fines.models import Fine

register = template.Library()


@register.filter
def is_fine(entity):
    return isinstance(entity, Fine)
