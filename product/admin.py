from django.contrib import admin
from .models import (
    Category, SubCategory, Company, Coupon,
    Product, Tag, Review, ProductQueries, WishList
)

# -------------------------
# CATEGORY
# -------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_popular", "slug")
    search_fields = ("name",)
    list_filter = ("is_popular",)
    prepopulated_fields = {"slug": ("name",)}


# -------------------------
# SUB CATEGORY
# -------------------------
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "sub_slug")
    search_fields = ("name", "category__name")
    list_filter = ("category",)
    prepopulated_fields = {"sub_slug": ("name",)}


# -------------------------
# COMPANY
# -------------------------
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "nationality", "is_bestseller", "slug")
    search_fields = ("name", "nationality")
    list_filter = ("is_bestseller",)
    prepopulated_fields = {"slug": ("name",)}


# -------------------------
# COUPON
# -------------------------
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("name", "coupon_types", "value", "expire_at")
    search_fields = ("name",)
    list_filter = ("coupon_types", "expire_at")


# -------------------------
# PRODUCT
# -------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "stock_quantity",
        "sell_quantity",
        "remaining_quantity",
        "price",
        "stock_status",
        "created_at",
    )
    search_fields = ("title", "category__name", "company__name", "SKU")
    list_filter = ("category", "sub_category", "stock_status", "language", "top_selling")
    filter_horizontal = ("company",)
    
    readonly_fields = ("remaining_quantity", "created_at",)
    prepopulated_fields = {"slug": ("title",)}


# -------------------------
# TAG
# -------------------------
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("tag",)
    search_fields = ("tag",)


# -------------------------
# REVIEW
# -------------------------
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "star_count", "post_date")
    search_fields = ("product__title", "user__username")
    list_filter = ("star_count", "post_date")


# -------------------------
# PRODUCT QUERIES
# -------------------------
@admin.register(ProductQueries)
class ProductQueriesAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "question", "answer")
    search_fields = ("product__title", "user__username", "question")


# -------------------------
# WISHLIST
# -------------------------
@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ("user", "product")
    search_fields = ("user__username", "product__title")
