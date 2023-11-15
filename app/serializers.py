from rest_framework import serializers
from app.models import CustomUser
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode as decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()
    class Meta:
        model = CustomUser
        fields = ['phone','password','password2','email']

    def validate(self, attrs):
         password1 = attrs.get('password')
         password2 = attrs.get('password2')
         if password1 != password2:
             return serializers.ValidationError('passwords do not match')
         return attrs

    def create(self, validated_data):
        password = validated_data.get('password')
        phone = validated_data.get('phone')
        email = validated_data.get('email')
        return CustomUser.objects.create_user(password=password, phone=phone, email=email)


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()


class SendResetPasswordLinkSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def validate_email(self, email):
        result = CustomUser.objects.filter(email=email).exists()
        if not result:
            raise serializers.ValidationError('Please enter your registered email')
        else:
            return email

class ResetPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')

        if password1 != password2:
            raise serializers.ValidationError('Passwords do not match')
        
        uid = self.context['uid']
        token = self.context['token']

        id = smart_str(decode(uid))
        user = CustomUser.objects.get(id=id)
        result = PasswordResetTokenGenerator().check_token(user,token)
        

        if not result:
            raise serializers.ValidationError("Token is not valid or expired")

        user.set_password(password1)
        user.save()
        return attrs

