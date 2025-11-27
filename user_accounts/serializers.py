from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate


class CustomUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    full_name = serializers.CharField(style={'input_type':'text'},write_only=True)
    uuid = serializers.UUIDField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['uuid', 'password', 'password2', 'username', 'full_name']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        
        username = validated_data.get("username")
        full_name = validated_data.get("full_name")
        
        
        validated_data['email'] = username
        user = CustomUser.objects.create(username= username, email= username,full_name=full_name)
        user.set_password(validated_data['password'])
        user.save()
        # refer_code =  str(random.randint(100011, 999999))
        # send_refer_code(refer_code= refer_code, email =username)
        # EmailTokens.objects.create(email=username,token=refer_code)

        
      

        return user
    


class UserLoginSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField()
    password = serializers.CharField()
    

    
    class Meta:
        model = CustomUser
        fields = ['username','password'] #username is email
        
    
    def validate(self, data):
        print(data)
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect username and password")


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data.get('new_password') != data.get('confirm_password'):
            raise serializers.ValidationError("New password and confirm password must match.")
        return data

class ForgotPasswordLinkSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    

# from rest_framework import serializers
# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from dj_rest_auth.registration.serializers import SocialLoginSerializer

# class GoogleLoginSerializer(SocialLoginSerializer):
#     code = serializers.CharField(required=True, trim_whitespace=True)

#     def validate(self, attrs):
#         adapter_class = GoogleOAuth2Adapter
#         provider_class = adapter_class.get_provider()
#         client = provider_class(self.request)
#         data = client.get_access_token(attrs['code'])
#         return data
