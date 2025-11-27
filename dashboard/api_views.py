from product.serializers import *
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser,AllowAny
from rest_framework.response import Response
from product.models import *
from user_accounts.serializers import CustomUserListSerializer
from website.models import *
from website.serializers import *
from user_accounts.models import *
from rest_framework.pagination import PageNumberPagination
from order.models import Orders
from order.serializers import OrderSerializer
from rest_framework import status
from rest_framework.views import APIView
from datetime import datetime,timedelta
from blog.models import *
from blog.serializers import *




class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100



class DashboardCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = BookCategorySerializer
    permission_classes =[IsAdminUser]
    lookup_field = 'slug'

class DashboardSubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = BookSubCatagoriesSerializer
    permission_classes =[IsAdminUser]
    lookup_field = 'sub_slug'

class DashboardAuthorViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    pagination_class = CustomPagination
    permission_classes = [IsAdminUser]

class DashboardCouponViewSet(viewsets.ModelViewSet):
    queryset=Coupon.objects.all()
    serializer_class=CouponSerializer
    permission_classes = [IsAdminUser]

class DashboardProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    permission_classes =[IsAdminUser]
    lookup_field = 'slug'

class DashboardProductQueriesViewSet(viewsets.ModelViewSet):
    queryset=ProductQueries.objects.all()
    serializer_class=ProductQueriesSerializer
    permission_classes =[IsAdminUser]
    
class DashboardProductReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = CustomPagination
    permission_classes =[IsAdminUser]

class DashboardCustomUserList(viewsets.ReadOnlyModelViewSet):
    serializer_class = CustomUserListSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination
    queryset = CustomUser.objects.all()

class DashboardMenusViewSet(viewsets.ModelViewSet):
    queryset = Menus.objects.all()
    serializer_class = MenusSerializer
    permission_classes = [IsAdminUser]

class DashboardFaqsViewSet(viewsets.ModelViewSet):
    queryset = Faqs.objects.all()
    serializer_class = FaqsSerializer
    permission_classes = [IsAdminUser]

class DashboardFaqsTopicViewSet(viewsets.ModelViewSet):
    queryset = FaqsTopic.objects.all()
    serializer_class = FaqsTopicSerializer
    permission_classes = [IsAdminUser]

class DashboardCarousalViewSet(viewsets.ModelViewSet):
    queryset = Carousal.objects.all()
    serializer_class = CarousalSerializer
    permission_classes = [IsAdminUser]

class DashboardCareersViewSet(viewsets.ModelViewSet):
    queryset = Careers.objects.all()
    serializer_class = CareersSerializer
    permission_classes = [IsAdminUser]

class DashboardTermsAndConditionViewSet(viewsets.ModelViewSet):
    queryset = TermsAndCondition.objects.all()
    serializer_class = TermsAndConditionSerializer
    permission_classes = [IsAdminUser]

class DashboardPrivacyPolicyViewSet(viewsets.ModelViewSet):
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicySerializer
    permission_classes = [IsAdminUser]

class DashboardNewsletterViewSet(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [IsAdminUser]


class DashboardOrder(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'uuid'
    http_method_names = ('put','patch','get')


class AnalyticsAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, format=None):
        # Total Sales
        total_sales = Orders.objects.filter(status='Delivered').count()
        pending_orders = Orders.objects.filter(status='Pending').count()
        rejected_orders = Orders.objects.filter(status__in=['Rejected','Cancelled']).count()
        total_sell_amount = Orders.objects.filter(status='Delivered').aggregate(total_sell_amount=models.Sum('amount_to_pay'))['total_sell_amount'] or 0

        # Calculate total shipping charge for delivered orders
        total_shipping_charge = Orders.objects.filter(status='Delivered').aggregate(total_shipping_charge=models.Sum('shipping_charge'))['total_shipping_charge'] or 0



        # Total Profit

        # Total Active Users
        start_date = datetime.now().date() - timedelta(days=30)

        # Count active users who have performed some actions within the time period
        total_active_users = CustomUser.objects.filter(last_login__gte=start_date).count()
        # Daily Sales Analytics
        today = datetime.now().date()
        daily_sales_analytics = []
        for i in range(7):
            date = today - timedelta(days=i)
            daily_sales_count = Orders.objects.filter(status='Delivered', created_at__date=date).count()
            daily_sales_analytics.append({'date': date, 'sales_count': daily_sales_count})

        # Monthly Sales Analytics
        monthly_sales_analytics = []
        for i in range(6, -1, -1):
            date = today - timedelta(days=i * 30)
            month = date.strftime('%B')
            monthly_sales_count = Orders.objects.filter(status='Delivered', created_at__month=date.month).count()
            monthly_sales_analytics.append({'month': month, 'sales_count': monthly_sales_count})

        data = {
            'total_sales': total_sales,
            'pending_orders': pending_orders,
            'rejected_orders': rejected_orders,
            'total_sell_amount': total_sell_amount,
            'total_shipping_charge': total_shipping_charge,
            'total_active_users': total_active_users,
            'daily_sales_analytics': daily_sales_analytics,
            'monthly_sales_analytics': monthly_sales_analytics,
            
        }

        return Response(data)
    

# Blog Section

class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes =[IsAdminUser]

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes =[IsAdminUser]
    lookup_field = 'slug'

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes =[IsAdminUser]
    permission_classes = ('get','put','patch')

    def get_queryset(self):
        queryset = super().get_queryset()
        post_id = self.request.query_params.get('post_id')
        post = Blog.objects.filter(id=post_id)
        if post_id:
            queryset = queryset.filter(post_id=post)
            return queryset
        else:
            return None
        

class OrderRejectedViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    http_method_names = ['put']
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'uuid'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'Rejected'
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
class OrderAcceptedViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['put']
    lookup_field = 'uuid'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'Accepted'
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)