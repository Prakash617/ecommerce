
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    
)
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
from product.api_views import ProductSearchAPIView
from dashboard.api_views import AnalyticsAPIView
from user_accounts.api_views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework_social_oauth2.urls',namespace='rest_framework_social_oauth2')),
    path('order/',include('order.api_urls')),
    path('inventory/',include('inventory.api_urls')),
    path('product/', include('product.api_urls')),
    path('website/',include('website.api_urls')),
    path('dashboard/',include('dashboard.api_urls')),
    path('users/',include('user_accounts.api_urls')),
    path('blogs/',include('blog.api_urls')),    
    path('payment/',include('payment.api_urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('summernote/', include('django_summernote.urls')),
    path('social-auth/',include('social_django.urls',namespace='social')),
    path('api/product/search/', ProductSearchAPIView.as_view(), name='product_search'),
    path('api/dashboard/analytics/', AnalyticsAPIView.as_view(), name='analytics'),
    path('api/user/forgot-password_link/', ResetPasswordLinkViewSet.as_view(), name='forgot_password_link'),
    path('api/user/forgot-password/', ResetPasswordView.as_view(), name='forgot_password'),
    
    path('api/user/authentication/',SocialLogin.as_view(),name='user_authenticate'),


    

    # ------------------jwt------------
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/', include(router.urls)),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)