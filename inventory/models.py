from django.db import models
from product.models import Product

# Create your models here.
# sold qty
# qty
# purchase unit price
# product

class SupplierData(models.Model):
    name = models.CharField(max_length=99)
    contact = models.CharField(max_length=99, unique=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=99, null=True)

    def __str__(self):
        return self.name
    

class Supply(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    buy_price = models.IntegerField()
    supplier = models.ForeignKey(SupplierData, related_name='supply', on_delete=models.CASCADE ,null=True)
    
    def __str__(self):
        return self.product.title