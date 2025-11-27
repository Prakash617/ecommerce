from .models import *
from rest_framework import serializers
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class CareersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Careers
        fields = "__all__"

class MenusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menus
        fields = "__all__"

class CarousalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousal
        fields = "__all__"

class FaqsTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaqsTopic
        fields = "__all__"
        
class FaqsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faqs
        fields = "__all__"

class TopicFaqsSerializer(serializers.ModelSerializer):
    faqs = FaqsSerializer(many=True,read_only=True,source='faqs_set')
    class Meta:
        model = FaqsTopic
        fields = ('id','title','faqs')

class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'

# class SummernoteField(serializers.CharField):
#     widget = SummernoteWidget()

class TermsAndConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsAndCondition
        fields = '__all__'

class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = '__all__'