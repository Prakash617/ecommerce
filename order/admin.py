from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(OrderQuantity)
admin.site.register(Orders)
admin.site.register(CustomerAddress)
admin.site.register(PaymentDetail)