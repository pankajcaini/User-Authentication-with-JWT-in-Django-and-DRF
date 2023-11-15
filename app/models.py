from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone, password, **other):
        user = self.model(phone=phone,**other)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password, **other):
        other.setdefault('is_staff',True)
        other.setdefault('is_active',True)
        other.setdefault('is_superuser', True)
        return self.create_user(phone, password, **other)


class CustomUser(AbstractBaseUser):
    phone = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'

    objects = UserManager()

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True
