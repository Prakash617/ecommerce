from .serializers import *
from rest_framework import viewsets,generics
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from dashboard.api_views import CustomPagination
from order.models import Orders
from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import PermissionDenied
from rest_framework import status


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = BookCategorySerializer
    permission_classes =[AllowAny]
    lookup_field = 'slug'

class PopularCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BookCategorySerializer
    permission_classes =[AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Category.objects.filter(is_popular=True)
        return queryset

    

class SubCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = BookSubCatagoriesSerializer
    permission_classes =[AllowAny]
    lookup_field = 'sub_slug'

class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Company.objects.filter(is_bestseller=True)
        return queryset

class CouponViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=Coupon.objects.all()
    serializer_class=CouponSerializer
    permission_classes = [AllowAny]

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    permission_classes =[AllowAny]
    lookup_field = 'slug'

class UsedBookViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Product.objects.filter(is_used=True)
        category = self.request.query_params.get('category')
        sub_category = self.request.query_params.get('sub_category')
        language = self.request.query_params.get('language')
        
            
        
        
        if language:
    
            languages = [s.strip() for s in language.split(',')]
            
            queryset = queryset.filter(language__in=languages)
                
        if category:

            queryset = Product.objects.filter(category__slug__icontains=category,is_used=True)
  
            if sub_category:
                sub_categories = [s.strip() for s in sub_category.split(',')]
                queryset = queryset.filter(sub_category__name__in=sub_categories)

                if language:
    
                    languages = [s.strip() for s in language.split(',')]
            
                    queryset = queryset.filter(language__in=languages)
                
        return queryset
    
class BestSellerBookViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    permission_classes =[AllowAny]
    pagination_class = CustomPagination
    lookup_field = 'slug'
    
    def get_queryset(self):
        queryset = Product.objects.filter(top_selling=True)
        return queryset

class NewArrivalBookViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    permission_classes =[AllowAny]
    pagination_class = CustomPagination
    lookup_field = 'slug'
    
    def get_queryset(self):
        queryset = Product.objects.filter(new_arrival=True)
        return queryset

class NepaliBookViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    permission_classes =[AllowAny]
    pagination_class = CustomPagination
    lookup_field = 'slug'
    
    def get_queryset(self):
        queryset = Product.objects.filter(language="Nepali")
        return queryset

class AuthorBookViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = CustomPagination
    lookup_field = 'slug'

    def get_queryset(self):
        author_slug = self.request.query_params.get('author')
        print("hello",author_slug)
        if author_slug:
            queryset = Product.objects.filter(authors__slug__icontains=author_slug)
        else:
            queryset = Product.objects.none()
        
        return queryset

    

class SubCategoryBookViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = CustomPagination
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        sub_category = self.request.query_params.get('sub_category')
        category = self.request.query_params.get('category')
        language = self.request.query_params.get('language')
        try:

            if category:

                queryset = Product.objects.filter(category__slug__icontains=category)
    
                if sub_category:
                    sub_categories = [s.strip() for s in sub_category.split(',')]
                    queryset = queryset.filter(sub_category__name__in=sub_categories)
    
                if language:
    
                        languages = [s.strip() for s in language.split(',')]
                
                        queryset = queryset.filter(language__in=languages)
            else:
                queryset = Product.objects.none()

        except:
            queryset = Product.objects.none()
        
        return queryset


class ProductQueriesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=ProductQueries.objects.all()
    serializer_class=ProductQueriesSerializer
    
class ProductReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.IsAuthenticatedOrReadOnly()]

    def get_queryset(self):
        try:
            if self.action == 'list':
                product_id = self.request.query_params.get('product_id')
                product = Product.objects.get(id=product_id)
                return Review.objects.filter(product=product).order_by('-id')
        except:
            return Review.objects.none()
    def perform_create(self, serializer):
        product_id = self.request.data.get('product')
        user = self.request.user

        # Check if the user has bought the product
        try:
            if Orders.objects.filter(customer=user, order_qty__product_id=product_id,status='Delivered').exists():
                serializer.save(user=user)
            else:
                raise PermissionDenied("You have not bought this product yet. You have to order this product before giving rating.")
        except ObjectDoesNotExist as e:
            # Log the error or handle it as per your requirement
            pass


class WishListViewSet(viewsets.ModelViewSet):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        product_id = self.request.data.get('product')

        # Check if the product already exists in the wishlist
        if WishList.objects.filter(user=user, product_id=product_id).exists():
            raise serializers.ValidationError('Product already exists in the wishlist.')

        serializer.save(user=user)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return WishList.objects.filter(user=user)
    
class ProductSearchAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination


    def get_queryset(self):
        queryset = Product.objects.all()

        query = self.request.query_params.get('query', None)
        search_by = self.request.query_params.get('search_by', None)
        if not query or not search_by:
            return None
        if search_by == 'product':
            queryset = queryset.filter(title__icontains=query) | queryset.filter(isbn_number__icontains=query)
        elif search_by == 'company':
            queryset = queryset.filter(authors__slug__icontains=query)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif not queryset.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)



