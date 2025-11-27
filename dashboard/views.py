from django.shortcuts import render
from order.models import Orders
from django.views.generic import DetailView

# Create your views here.

class PrintInvoiceView(DetailView):
    model = Orders
    template_name = "billing/order_invoice.html"
    # pk_url_kwarg = 'uuid'

class ShippingLabelView(DetailView):
    model = Orders
    template_name = "billing/order_shipping_label.html"
    # pk_url_kwarg = 'uuid'
