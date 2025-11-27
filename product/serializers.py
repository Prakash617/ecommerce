from rest_framework import serializers
from .models import *



# class BookCatagoriesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = "__all__"

class BookSubCatagoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"

class BookCategorySerializer(serializers.ModelSerializer):
    subcategories = BookSubCatagoriesSerializer(many=True, read_only=True,source='subcategory_set')

    class Meta:
        model = Category
        fields = ('id', 'name', 'icon','slug', 'subcategories')


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

class CouponSerializer(serializers.ModelSerializer):

    class Meta:
        model= Coupon
        fields= '__all__'
        

class ProductQueriesSerializer(serializers.ModelSerializer):
    class Meta:
        model= ProductQueries
        fields= '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'profile']

        
class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False,read_only=True)
    post_date = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'star_count', 'review_text', 'post_date', 'product']

    def get_post_date(self, obj):
        return obj.post_date.strftime('%d %B %Y')




        
class ProductSerializer(serializers.ModelSerializer):
    # category = BookCatagoriesSerializer(many=False, read_only=True)
    authors = CompanySerializer(many=True,read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        product_id = data['id']
        product = Product.objects.get(id=product_id)
        book_review = Review.objects.filter(product=product)
        total_book_review = Review.objects.filter(product=product).count()
        total_rating = 0
        for book in book_review:
            rate = book.star_count
            total_rating += rate
        if total_book_review:
            average_rating = total_rating/total_book_review
        else:
            average_rating = 0
            
        

        authors_data = data.pop('authors')
        author_names = [author['name'] for author in authors_data]
        data['authors'] = author_names
        data['total_book_review'] = total_book_review
        data['average_rating'] = average_rating
        return data
        

class WishListSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = WishList
        fields = ['id','product', 'product_details']  
