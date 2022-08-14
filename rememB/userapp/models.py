from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(self, email, username, provider, birth, refreshToken, password=None):
        if not email:
            raise ValueError('The Email must be set')
        if not provider:
            raise ValueError('The Social Auth must be set')
        
        user=self.model(
            email=self.normalize_email(email),
            username=username,
            provider=provider,
            birth=birth,
        )
        user.set_unusable_password()
        return user
    
    def create_superuser(self, email, username, provider, birth, refreshToken, password=None):
        user=self.model(
            email=self.normalize_email(email),
            username=username,
            provider=provider,
            birth=birth,
        )
        user.set_unusable_password()
        user.is_admin=True
        return user


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True,)
    email=models.EmailField(verbose_name=('email'), max_length=64, unique=True, null=False, blank=False,)
    username=models.CharField(max_length=30, null=False, blank=False,)
    provider=models.CharField(max_length=20, null=False, blank=False,)
    birth=models.DateField(blank=True,)
    refreshToken=models.CharField(max_length=2000, null=True, default='',)
    password=models.CharField(null=True, max_length=100)

    # User 모델의 필수 field
    is_active = models.BooleanField(default=True)    
    is_admin = models.BooleanField(default=False)
    
    objects=UserManager()

    def __str__(self):
        return str(self.email)
    
    def get_id(self):
        return str(self.id)
    
    def validate(self,data):
        search_email=data.get('email',None)
        if User.objects.filter(email=search_email).exists():
            print('이미 있는 아이디입니다.')
        return data
    
    @property
    def is_staff(self):
        return self.is_admin

