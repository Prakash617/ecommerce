from django.db import models
from product.models import Product
from django.contrib.auth.models import User
import uuid
import datetime
from user_accounts.models import CustomUser


country_choices = (
    ('Nepal', 'Nepal'),
)

CITY_CHOICES = (
    ('Pokhara', 'Pokhara'),
    ('Kathmandu', 'Kathmandu'),
    ('Biratnagar', 'Biratnagar'),
    ('Birgunj', 'Birgunj'),
    ('Hetauda', 'Hetauda'),
    ('Butwal', 'Butwal'),
    ('Bhairahawa', 'Bhairahawa'),
    ('Nepalgunj', 'Nepalgunj'),
    ('Bharatpur', 'Bharatpur'),
    ('Dhangadi', 'Dhangadi'),
    ('Dharan', 'Dharan'),
    ('Itahari', 'Itahari'),
    ('Damak', 'Damak'),
    ('Birtamode', 'Birtamode'),
    ('Janakpur', 'Janakpur'),
    ('Bardia', 'Bardia'),
    ('Dang', 'Dang'),
    ('Dhulikhel', 'Dhulikhel'),
    ('Bhaktapur', 'Bhaktapur'),
    ('Lalitpur', 'Lalitpur'),
    ('Surkhet', 'Surkhet'),
    ('Damauli', 'Damauli'),
    ('Banepa', 'Banepa'),
    ('Ghorai', 'Ghorai'),
    ('Bardaghat', 'Bardaghat'),
    ('Chandragadi', 'Chandragadi'),
    ('Parasi', 'Parasi'),
    ('Bhadrapur', 'Bhadrapur'),
    ('Sunawal', 'Sunawal'),
    ('Kakarvitta', 'Kakarvitta'),
    ('Kalaiya', 'Kalaiya'),
    ('Tilotama', 'Tilotama'),
    ('Lumbini', 'Lumbini'),
    ('Tulsipur', 'Tulsipur'),
    ('Narayanghat', 'Narayanghat'),
    ('Urlabari', 'Urlabari'),
    ('Nawalparasi', 'Nawalparasi')
)


class OrderQuantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.CharField(max_length=9999)
    initial_price = models.FloatField()
    
    def __str__(self):
        return f"Order for {self.quantity}"

    class Meta:
        verbose_name = "Order Quantity"
        verbose_name_plural = "Order Quantities"


class CustomerAddress(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=9999, blank=True, null=True)
    email = models.CharField(max_length=99, blank=True, null=True)
    phone = models.CharField(max_length=9999, blank=True, null=True)
    address_line_1 = models.CharField(max_length=9999, blank=True, null=True)
    address_line_2 = models.CharField(max_length=9999, blank=True, null=True)
    city = models.CharField(max_length=9999, choices=CITY_CHOICES)
    country = models.CharField(max_length=9999, choices=country_choices, default="Nepal")
    is_default = models.BooleanField(default=False, null=True)

    def __str__(self):
        address_parts = [self.address_line_1, self.address_line_2, self.city, self.country]
        non_none_address_parts = filter(lambda part: part is not None, address_parts)
        return ', '.join(map(str, non_none_address_parts))

    class Meta:
        verbose_name = "Customer Address"
        verbose_name_plural = "Customer Addresses"


STATUS = (
    ('All', 'All'),
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
    ('Rejected', 'Rejected'),
    ('Cancelled', 'Cancelled'),
    ('Failed', 'Failed'),
)
 
    
PAYMENT_METHOD_CHOICES = (
    ('Cash On Delivery', 'Cash On Delivery'),
    ('Khalti', 'Khalti'),
)


class PaymentDetail(models.Model):
    order_id = models.CharField(max_length=9999, null=True, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=9999, choices=PAYMENT_METHOD_CHOICES, default="Cash On Delivery")
    amount = models.FloatField()
    transaction_id = models.CharField(max_length=9999)
    status = models.CharField(max_length=9999, null=True, blank=True)
    payment_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    payment_url = models.URLField(null=True, blank=True)
    details = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Payment for Order ID: {self.order_id}"

    class Meta:
        verbose_name = "Payment Detail"
        verbose_name_plural = "Payment Details"


class Orders(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    order_qty = models.ManyToManyField(OrderQuantity)
    initial_price = models.FloatField(null=True, blank=True)
    discount = models.FloatField(null=True, blank=True)
    amount_to_pay = models.FloatField(null=True, blank=True)
    coupon = models.CharField(max_length=9999, null=True, blank=True)
    tax = models.FloatField(null=True, blank=True)
    address = models.ForeignKey(CustomerAddress, on_delete=models.CASCADE, null=True, blank=True)
    shipping_charge = models.FloatField(default=0.00)
    status = models.CharField(max_length=9999, choices=STATUS, default="Pending")
    payment_details = models.OneToOneField(PaymentDetail, related_name='order', on_delete=models.CASCADE, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    remarks = models.CharField(max_length=33, blank=True)
    delivered_date = models.DateTimeField(null=True, blank=True)
    is_payment_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk:
            old_order = Orders.objects.get(pk=self.pk)
            if old_order.status != 'Cancelled' and self.status == 'Cancelled':
                self.update_product_sell_quantity(decrease=True)
            elif old_order.status != 'Rejected' and self.status == 'Rejected':
                self.update_product_sell_quantity(decrease=True)

        if self.pk:
            original_order = Orders.objects.get(pk=self.pk)
            if original_order.status != 'Delivered' and self.status == 'Delivered':
                self.delivered_date = datetime.datetime.now()

        super(Orders, self).save(*args, **kwargs)

    def update_product_sell_quantity(self, decrease=False):
        for order_qty in self.order_qty.all():
            product = order_qty.product
            if product is not None:
                if decrease:
                    product.sell_quantity -= int(order_qty.quantity)
                    product.save()

    def __str__(self):
        return f"Order {self.id} by {self.customer}"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
