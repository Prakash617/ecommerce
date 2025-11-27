from rest_framework import serializers
from .models import Supply,SupplierData


class SupplierDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SupplierData
        fields = '__all__'

class SupplySerializer(serializers.ModelSerializer):
    product_stock_quantity = serializers.ReadOnlyField(source='product.stock_quantity')
    product_sell_quantity = serializers.ReadOnlyField(source='product.sell_quantity')
    remaining_quantity = serializers.SerializerMethodField()

    def get_remaining_quantity(self, obj):
        return obj.product.stock_quantity - obj.product.sell_quantity

    class Meta:
        model = Supply
        fields = ['id', 'product', 'buy_price', 'supplier', 'product_stock_quantity', 'product_sell_quantity', 'remaining_quantity']
