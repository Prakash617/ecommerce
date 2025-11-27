from django.urls import include, path

from user_accounts.api_views import *
from bookstore.urls import router

router.register(r'user/register',UserRegister,basename='registration')
router.register(r'user/login',UserLoginViewSet,basename='login')
router.register(r'user/my_details',MyDetailsViewSet,basename='my_details')
router.register(r'user/verify',UserVerificationViewSet, basename='verify-user')
router.register(r'user/change_password',UserChangePasswordViewSet, basename='password_change-user')




urlpatterns = [
    path('api/', include(router.urls)),
    path('home/', home, name='home'),
    
]