from django.urls import include, path

from product.api_views import *
from bookstore.urls import router

router.register(r'product/categories',CategoryViewSet,basename='catogories')
router.register(r'product/popular_categories',CategoryViewSet,basename='popular_categories')
router.register(r'product/subcategories',SubCategoryViewSet,basename='subcategories')
router.register(r'product/best_company',CompanyViewSet,basename='best_company')
router.register(r'product/products',ProductViewSet,basename='product')
router.register(r'product/queries',ProductQueriesViewSet,basename='product_queries')
router.register(r'product/review',ProductReviewViewSet,basename='product_review')
router.register(r'coupon/coupons',CouponViewSet,basename='book_coupon')
router.register(r'product/used_product',UsedBookViewSet,basename='used_product')
router.register(r'product/new_arrival_product',NewArrivalBookViewSet,basename='new_arrival_product')
router.register(r'product/nepali_product',NepaliBookViewSet,basename='nepali_product')
router.register(r'product/best_seller_product',BestSellerBookViewSet,basename='best_seller_product')
router.register(r'product/company_product',AuthorBookViewSet,basename='company_product') #?author
# router.register(r'book/category_books',CategoryBookViewSet,basename='category_books') #?category
router.register(r'product/category_product',SubCategoryBookViewSet,basename='category_product') #?sub_category
router.register(r'product/wish_list',WishListViewSet,basename='wish_list') 




urlpatterns = [
    path('api/', include(router.urls)),
    
    
   
]