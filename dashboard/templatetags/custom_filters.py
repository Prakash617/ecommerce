from django.utils.timesince import timesince
from django.template import Library

from order.models import OrderQuantity, Orders

register = Library()

@register.filter
def time_ago_format(value):
    return timesince(value)


@register.filter
def discount_calculator(id):
    order = Orders.objects.get(id=id)
    if order.initial_price:
        return order.initial_price - order.amount_to_pay
    else:
        return None
    
@register.filter
def get_invoice_number(value):
    return 1000 + int(value)


@register.filter
def get_product_price(value):
    current_qty_data = OrderQuantity.objects.get(id=value)
    return float(current_qty_data.quantity) * current_qty_data.initial_price

@register.filter
def limit_size(text,size):
    if len(text) > size:
        return text[:size] + "..."
    return text

