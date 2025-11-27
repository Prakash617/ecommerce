from django.urls import include, path

from inventory.api_views import *
from bookstore.urls import router


router.register(r'inventory/supplier_data',SupplierDataViewSet, basename='supplier_data')
router.register(r'inventory/supply',SupplyViewSet, basename='supply')




urlpatterns = [
    path('api/', include(router.urls)),
   
]