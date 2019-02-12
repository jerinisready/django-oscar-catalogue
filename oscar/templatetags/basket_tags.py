from django import template

from oscar.core.loading import get_class, get_model


Product = get_model('catalogue', 'product')

register = template.Library()

QNT_SINGLE, QNT_MULTIPLE = 'single', 'multiple'


@register.simple_tag
def basket_form(request, product, quantity_type='single'):
    return
