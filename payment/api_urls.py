from django.urls import include, path
from .api_views import VerifyKhalti





urlpatterns = [
    path('api/verify-khalti/', VerifyKhalti.as_view(), name='verify_khalti'),
   
]