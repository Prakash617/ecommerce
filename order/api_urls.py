from django.urls import include, path

from order.api_views import *
from bookstore.urls import router

router.register(r'order/guest_checkout',GuestOrderViewSet,basename='guest_checkout')
router.register(r'order/login_user_checkout',LoginUserOrderViewSet,basename='login_user_checkout')
router.register(r'order/track_myorder',OrdersTrackingViewSet,basename='track_myorder')
router.register(r'order/my_active_orders',MyActiveOrderViewSet,basename='my_active_order')
router.register(r'order/old_orders',MyOldOrderViewSet,basename='old_order')
router.register(r'order/my_address',MyAddressViewSet,basename='my_address')





urlpatterns = [
    path('api/', include(router.urls)),
   
]