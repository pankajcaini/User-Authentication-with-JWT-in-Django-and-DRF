from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from app.serializers import UserRegistrationSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from app.serializers import UserChangePasswordSerializer, SendResetPasswordLinkSerializer, ResetPasswordSerializer
from app.models import CustomUser
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode as encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.hashers import make_password, check_password

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access':str(refresh.access_token),
        'refresh':str(refresh)
    }

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("User created")
        else:
            return Response(serializer.errors)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data.get('phone')
            password = serializer.validated_data.get('password')
            print(phone,password)
            user = authenticate(phone=phone, password=password)
            if user is not None:
                return Response(get_tokens_for_user(user))
            else:
                return Response("Phone or Password is incorrect")
        else:
            return Response(serializer.errors)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response("user profile")


# user must be logged in
class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        print(request.user.password)
        serializer = UserChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            password = serializer.validated_data.get('password')
            user.set_password(password)
            user.save()
            return Response("password change successfully")
        else:
            return Response(serializer.errors)




# when user is not logged in
class SendResetPasswordLinkView(APIView):
    def post(self, request):
        serializer = SendResetPasswordLinkSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomUser.objects.get(email=email)

            id = user.id
            uid = encode(force_bytes(id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://127.0.0.1:8000/reset_password/' + uid + '/' + token

            return Response({'link':link})
        else:
            return Response(serializer.errors)

class ResetPasswordView(APIView):
    def post(self, request, uid, token):
        serializer = ResetPasswordSerializer(data=request.data, context={'uid':uid, 'token':token})
        if serializer.is_valid():
            return Response("password has been reset")
        else:
            return Response(serializer.errors)