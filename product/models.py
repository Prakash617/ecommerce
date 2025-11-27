from django.db import models
from user_accounts.models import CustomUser
from django.utils.text import slugify
from django.core.validators import MinValueValidator


Language = (
    ('Nepali', 'Nepali'),
    ('English', 'English'),
    ('Hindi', 'Hindi'),
)

Stockchoice = (
    ('In stock', 'In stock'),
    ('Out of Stock', 'Out of Stock')
)

coupon_types = (
    ('Percentage Discount', 'Percentage Discount'),
    ('Flat Discount', 'Flat Discount'),
    ('Bulk Discount', 'Bulk Discount'),
    ('Free Shipping', 'Free Shipping'),
)


def default_coupon_details():
    return {"empty": "empty"}


# -------------------------
# CATEGORY
# -------------------------
class Category(models.Model):
    name = models.CharField(max_length=9999)
    icon = models.FileField(upload_to='category/', blank=True, default="authors/profile.jpg")
    slug = models.CharField(max_length=9999, unique=True, null=True, blank=True)
    is_popular = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


# -------------------------
# SUB CATEGORY
# -------------------------
class SubCategory(models.Model):
    name = models.CharField(max_length=9999)
    sub_slug = models.CharField(max_length=9999, unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.sub_slug:
            self.sub_slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Sub Category"
        verbose_name_plural = "Sub Categories"


# -------------------------
# COMPANY (replaces Author)
# -------------------------
class Company(models.Model):
    name = models.CharField(max_length=999)
    slug = models.CharField(max_length=9999, unique=True, blank=True)
    bio = models.TextField()
    image = models.FileField(upload_to='authors/', blank=True, default="authors/profile.jpg")
    nationality = models.CharField(max_length=99999, null=True, blank=True)
    is_bestseller = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"


# -------------------------
# COUPON
# -------------------------
class Coupon(models.Model):
    name = models.CharField(max_length=400)
    coupon_types = models.CharField(max_length=400, choices=coupon_types, default="Percentage Discount")
    value = models.FloatField(default=0.0)
    coupon_details = models.JSONField(default=default_coupon_details, null=True, blank=True)
    expire_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"


# -------------------------
# PRODUCT (formerly Book)
# -------------------------
class Product(models.Model):
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=9999)
    company = models.ManyToManyField(Company, related_name='products')   # FIXED (authors → company)
    description = models.TextField()
    product_image = models.FileField(upload_to='product/', blank=True, default="product/Product.jpg")
    SKU = models.CharField(max_length=9999, null=True, blank=True)
    stock_status = models.CharField(choices=Stockchoice, default="In stock", max_length=9999, blank=True, null=True)
    stock_quantity = models.IntegerField(default=1)
    sell_quantity = models.IntegerField(default=0)
    remaining_quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    price = models.FloatField()
    published_date = models.DateField(null=True, blank=True)
    edition = models.CharField(max_length=9999, null=True, blank=True)
    page_count = models.IntegerField(null=True, blank=True)
    isbn_number = models.CharField(max_length=9999, null=True, blank=True)
    weight = models.CharField(max_length=9999, null=True, blank=True)
    language = models.CharField(max_length=9999, choices=Language, default="English")
    top_selling = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=True)
    new_arrival = models.BooleanField(default=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.CharField(max_length=9999, unique=True, null=True, blank=True)
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        self.remaining_quantity = self.stock_quantity - self.sell_quantity

        if self.remaining_quantity <= 0:
            self.stock_status = "Out of Stock"
        else:
            self.stock_status = "In stock"

        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


# -------------------------
# TAG
# -------------------------
class Tag(models.Model):
    product = models.ManyToManyField(Product)   # FIXED
    tag = models.CharField(max_length=75, unique=True)
    
    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


# -------------------------
# REVIEW
# -------------------------
class Review(models.Model):
    product = models.ForeignKey(Product, related_name='review_product', null=True, blank=True, on_delete=models.SET_NULL)  # FIXED
    user = models.ForeignKey(CustomUser, related_name='reviewing_customer', on_delete=models.CASCADE)
    star_count = models.IntegerField()
    review_text = models.CharField(max_length=9999)
    post_date = models.DateField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.product.title if self.product else "Review"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"


# -------------------------
# PRODUCT QUERIES
# -------------------------
class ProductQueries(models.Model):
    product = models.ForeignKey(Product, related_name='query_product', null=True, blank=True, on_delete=models.SET_NULL)  # FIXED
    user = models.ForeignKey(CustomUser, related_name='query_customer', on_delete=models.CASCADE)
    question = models.CharField(max_length=999)
    answer = models.CharField(max_length=999)
    
    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Product Query"
        verbose_name_plural = "Product Queries"


# -------------------------
# WISHLIST
# -------------------------
class WishList(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='wishlist_product', null=True, blank=True, on_delete=models.SET_NULL)  # FIXED
    
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"
