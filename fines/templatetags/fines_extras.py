from django import template

from fines.models import Fine, Sponsor

register = template.Library()


@register.filter
def is_fine_instance(entity):
    return isinstance(entity, Fine)


@register.filter
def is_sponsor_instance(entity):
    return isinstance(entity, Sponsor)
