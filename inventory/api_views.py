from rest_framework import viewsets
from .models import Supply,SupplierData
from .serializers import SupplySerializer,SupplierDataSerializer


class SupplierDataViewSet(viewsets.ModelViewSet):
    queryset = SupplierData.objects.all()
    serializer_class = SupplierDataSerializer

class SupplyViewSet(viewsets.ModelViewSet):
    queryset = Supply.objects.all()
    serializer_class = SupplySerializer