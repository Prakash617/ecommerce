from django.urls import include, path

from dashboard.api_views import *
from bookstore.urls import router
from .views import *

router.register(r'dashboard/dashboard_categories',DashboardCategoryViewSet,basename='dashboard_categories')
router.register(r'dashboard/dashboard_subcategories',DashboardSubCategoryViewSet,basename='dashboard_subcategories')
router.register(r'dashboard/dashboard_author',DashboardAuthorViewSet,basename='dashboard_author')
router.register(r'dashboard/dashboard_product',DashboardProductViewSet,basename='dashboard_product')
router.register(r'dashboard/dashboard_queries',DashboardProductQueriesViewSet,basename='dashboard_queries')
router.register(r'dashboard/dashboard_review',DashboardProductReviewViewSet,basename='dashboard_review')
router.register(r'dashboard/coupons',DashboardCouponViewSet,basename='dashboard_coupon')
router.register(r'dashboard/user_list',DashboardCustomUserList,basename='user_list')
router.register(r'dashboard/dashboard_carousals',DashboardCarousalViewSet,basename='dashboard_carousals')
router.register(r'dashboard/dashboard_menus',DashboardMenusViewSet,basename='dashboard_menus')
router.register(r'dashboard/dashboard_careers',DashboardCareersViewSet,basename='dashboard_careers')
router.register(r'dashboard/dashboard_faqs',DashboardFaqsViewSet, basename='dashboard_faqs')
router.register(r'dashboard/dashboard_faqs_topic',DashboardFaqsTopicViewSet, basename='dashboard_faqs_topic')
router.register(r'dashboard/dashboard_privacy_policy',DashboardPrivacyPolicyViewSet, basename='dashboard_privacy_policy')
router.register(r'dashboard/dashboard_terms_condition',DashboardTermsAndConditionViewSet, basename='dashboard_terms_condition')
router.register(r'dashboard/dashboard_newsletter',DashboardNewsletterViewSet, basename='dashboard_newsletter')
router.register(r'dashboard/dashboard_order',DashboardOrder, basename='dashboard_order')
router.register(r'dashboard/order/reject',OrderRejectedViewSet,basename='reject')
router.register(r'dashboard/order/accept',OrderAcceptedViewSet,basename='accept')
router.register(r'dashboard/blog/category', BlogCategoryViewSet,basename='dashboard_category')
router.register(r'dashboard/blog/blogs', BlogViewSet,basename='dashboard_blogs')
router.register(r'dashboard/blog/comments', CommentViewSet,basename='dashboard_comments')





urlpatterns = [
    path('api/', include(router.urls)),
    
    # order - billing
    path('order/<int:pk>/invoice/print', PrintInvoiceView.as_view(), name="print-invoice-view"),
    path('order/<int:pk>/shipping-label/print', ShippingLabelView.as_view(), name="print-shipping-label-view"),


   
]