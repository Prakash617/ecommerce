from dashboard.models import *
from website.serializers import *
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class MenusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Menus.objects.all()
    serializer_class = MenusSerializer
    permission_classes = [AllowAny]

class FaqsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FaqsTopic.objects.all()
    serializer_class = TopicFaqsSerializer
    permission_classes = [AllowAny]


class CarousalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Carousal.objects.all()
    serializer_class = CarousalSerializer
    permission_classes = [AllowAny]

class CareersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Careers.objects.all()
    serializer_class = CareersSerializer
    permission_classes = [AllowAny]


class NewsletterViewSet(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    http_method_names = 'post'
    permission_classes = [AllowAny]


    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        if Newsletter.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=400)
        return super().create(request, *args, **kwargs)



class TermsAndConditionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TermsAndCondition.objects.all()
    serializer_class = TermsAndConditionSerializer
    permission_classes = [AllowAny]

class PrivacyPolicyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicySerializer
    permission_classes = [AllowAny]