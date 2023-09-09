from django.db import models
from django.utils import timezone
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta
import uuid
from django.urls import reverse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from django.db.models.signals import pre_save
from django.dispatch import receiver
import pytz
from datetime import datetime, time
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# class CustomUserManager(BaseUserManager):
    
#     def create_user(self, email, password, **extra_fields):
#         """
#         Create and save a User with the given email and password.
#         """
#         if not email:
#             raise ValueError(_('The Email must be set'))
#         # print(email, password,username,fname,lname,'hasha')
#         email = self.normalize_email(email)
#         fname = self.normalize_email(fname)

#         lname = self.normalize_email(lname)

#         # username = self.normalize_email(username)

#         # fname = self.model( **extra_fields)

#         # lname = self.model( **extra_fields)

#         # user = self.model(email=email,first_name=fname,last_name=lname,username=username, **extra_fields)
#         user = self.model(email=email, **extra_fields)
        
#         user.set_password(password)
#         user.save()
#         return user

#     def create_superuser(self, email, password, **extra_fields):
#         """
#         Create and save a SuperUser with the given email and password.
#         """
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError(_('Superuser must have is_staff=True.'))
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError(_('Superuser must have is_superuser=True.'))
#         return self.create_user(email, password, **extra_fields)



# def generate_referral_link(request: Request,referral_code) -> str:
    
	
# class User(AbstractBaseUser, PermissionsMixin):
#     USER_TYPE_CHOICES = (
#         (1, 'Admin'),
#         (2, 'Manager'),
#         (3, 'Sales'),
#         (4, 'Owner'),
#     )
#     user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)
#     # referred_by = models.CharField(max_length=100, blank=True)
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     date_joined = models.DateTimeField(default=timezone.now)
    
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     def save(self, *args, **kwargs):
#         # if self.user_type == 3 and not self.referral_code_bdm:
#         #     self.referral_code_bdm = uuid.uuid4()
#         if self.user_type == 3 and not self.referral_url:
#             self.referral_url = f'{settings.BASE_URL}{reverse("signup")}?ref={self.pk}'
#         super().save(*args, **kwargs)
    

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']

#     def __str__(self):
#         return self.email

#     def get_full_name(self):
#         return f"{self.first_name} {self.last_name}"

#     def get_short_name(self):
#         return self.first_name

#     def has_perm(self, perm, obj=None):
#         return True

#     def has_module_perms(self, app_label):
#         return True
