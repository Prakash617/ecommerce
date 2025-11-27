from rest_framework import serializers
from .models import *
from product.serializers import ProductSerializer
from user_accounts.serializers import CustomUserSerializer

class OrderQuantitySerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderQuantity
        fields = '__all__'

    def get_product(self, obj):
        return obj.product.title if obj.product else None


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = '__all__'

class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetail
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_qty = OrderQuantitySerializer(many=True, read_only = True)
    customer = CustomUserSerializer(many=False, read_only = True)
    payment_details = PaymentDetailSerializer(many=False, read_only = True)
    address = serializers.SerializerMethodField()
    class Meta:
        model= Orders
        fields= '__all__'

    def get_address(self, obj):
        return obj.address.address_line_1 if obj.address.address_line_1 else obj.address.city

