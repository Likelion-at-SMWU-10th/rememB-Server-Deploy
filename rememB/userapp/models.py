from os import access
from django.db import models
import uuid


class User(models.Model):
    id = models.AutoField(primary_key=True,)
    email=models.EmailField(verbose_name=('email'), max_length=64, unique=True, null=False, blank=False,)
    username=models.CharField(max_length=30, null=False, blank=False,)
    provider=models.CharField(max_length=20, null=False, blank=False,)
    birth=models.DateField(blank=True,)
    refreshToken=models.CharField(max_length=2000, null=True, default='',)

    # User 모델의 필수 field
    is_active = models.BooleanField(default=True)    
    is_admin = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.email)
    
    def get_id(self):
        return str(self.id)
    
    def validate(self,data):
        search_email=data.get('email',None)

        if User.objects.filter(email=search_email).exists():
            print('이미 있는 아이디입니다.')

        return data
