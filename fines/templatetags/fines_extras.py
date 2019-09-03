from django import template

from fines.models import Fine

register = template.Library()


@register.filter
def is_fine_instance(entity):
    return isinstance(entity, Fine)
