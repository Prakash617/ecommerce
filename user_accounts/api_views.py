from django.shortcuts import HttpResponse, render, HttpResponse,redirect
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import *
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import *
from .utils import send_verify_email,send_resetpassword_link
from bookstore.settings import ip
from rest_framework import generics
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from user_accounts.models import CustomUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
    'refresh': str(refresh),
    'access': str(refresh.access_token),
    }




class UserRegister(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ['post']
    permission_classes = [AllowAny]
    def create(self, request):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        email = user.username
        print(email)
        link = f"{ip}/api/user/verify?uuid={user.uuid}"
        print(link)
        send_verify_email(link= link, email =email,username=user.full_name)
        return Response({'token':token, 'msg':'Registration Successful', 'uuid': user.uuid}, status=status.HTTP_201_CREATED)


class UserLoginViewSet(viewsets.ModelViewSet):
    
    queryset = CustomUser.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    
    def list(self, request, *args, **kwargs):
        return Response({"error":"login_required"})
    

    def create(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        
        # username = serializer.data.get('username')
        # password = serializer.data.get('password')
        # user = authenticate(username=username, password=password)
        # if user is not None:
        token = get_tokens_for_user(user)
        return Response({'token':token, 'msg':f'Login Success', 'uuid': user.uuid}, status=status.HTTP_200_OK)
        # else:
            # return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)


class MyDetailsViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserListSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ('get','put','patch')
    

    def get_queryset(self):
        return CustomUser.objects.filter(pk=self.request.user.pk)



class UserVerificationViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]


    def list(self, request):
        id = request.GET.get('uuid', None)
        if id:
            try:
                user = CustomUser.objects.get(uuid= id)
                user.isEmailVerified = True
                user.save()
                return redirect('https://www.destinybookshub.com/')
               
            except CustomUser.DoesNotExist:
                return Response({'message': 'User not found'})
        else:
            return Response({'message': 'Please provide an user id'})
            




class UserChangePasswordViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ['patch']
    permission_classes = [IsAuthenticated]


    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data.get("old_password")
            new_password = serializer.validated_data.get("new_password")

            # Check if old password is correct
            if not user.check_password(old_password):
                return Response({"detail": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

            # Set new password and save
            user.set_password(new_password)
            user.save()
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ResetPasswordLinkViewSet(generics.GenericAPIView):
    serializer_class = ForgotPasswordLinkSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        try:
            user = CustomUser.objects.get(email=email)
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"https://www.destinybookshub.com//change_password/?token={uid}--{token}&email={user.email}"
    
            print(reset_url)
            
            send_resetpassword_link(reset_url, email =email)
            return Response({'message': 'An email with instructions for resetting your password has been sent.'})
        except CustomUser.DoesNotExist:
            return Response({"detail": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]


    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = request.GET.get('token', None)
        print("token",token)
        email = request.GET.get('email', None)
        password = serializer.validated_data.get('password')

        if not token:
            return Response({'error': 'Token not provided.'}, status=status.HTTP_400_BAD_REQUEST)

        # try:
        #     user = CustomUser.objects.get(email=email)
        # except CustomUser.DoesNotExist:
        #     return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            uidb64, token = token.split("--")
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid, email=email)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
        if default_token_generator.check_token(user, token):
            # Update user's password
            user.set_password(password)
            user.save()
            return Response({'message': 'Password has been successfully updated.'})
        else:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)


# from django.http import JsonResponse
# from django.views import View
# from rest_framework.decorators import api_view
# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from dj_rest_auth.registration.views import SocialLoginView
# from .serializers import GoogleLoginSerializer

# class CustomGoogleLoginView(SocialLoginView):
#     serializer_class = GoogleLoginSerializer

# class CustomLoginRedirectView(View):
#     def get(self, request, *args, **kwargs):
#         # Redirect to Google OAuth2 login URL
#         adapter = GoogleOAuth2Adapter()
#         login_url = adapter.get_login_url(request)
#         return JsonResponse({'login_url': login_url})

# class CustomLoginCallbackView(View):
#     def get(self, request, *args, **kwargs):
#         # Retrieve access token and user details after successful login
#         code = request.GET.get('code')
#         adapter = GoogleOAuth2Adapter()
#         user = adapter.complete_login(request, app=self.request)
#         access_token = user.token.token

#         # You can retrieve user details from user.account or user.user
#         user_details = {
#             'id': user.account.pk,
#             'email': user.account.extra_data.get('email'),
#             # Add other user details as needed
#         }

#         # Redirect to frontend with access token and user details
#         return JsonResponse({'access_token': access_token, 'user': user_details})

from social_django.models import UserSocialAuth
def home(request):
    social = Social.objects.create(user=request.user)
    code = social.code
    # return redirect(f'https://destiny-orpin.vercel.app/auth/?token={code}')
    return redirect(f'https://www.destinybookshub.com//auth/?token={code}')


class SocialLogin(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        code = request.data['code']
        print(code)
        try:
            user = Social.objects.get(code=code)
            uid = user.user.uuid
            token = get_tokens_for_user(user.user)
            user.delete()

            return Response({'token':token, 'msg':f'Login Success', 'uuid': uid}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
