from os import access
from django.db import models
import uuid

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

#uuid, email, provider, username, birth
class User(models.Model):
    uuid=models.UUIDField(
        #primary_key=True,
        default=uuid.uuid4,
        unique=True,
        db_index=True,
    )
    email=models.EmailField(
        verbose_name=('email'),
        max_length=64,
        unique=True,
        null=False,
        blank=False,
    )
    username=models.CharField(
        max_length=30,
        null=False,
        blank=False,
    )
    provider=models.CharField(
        max_length=20,
        null=False,
        blank=False,
    )
    birth=models.DateField(
        blank=True,
    )
    refreshToken=models.CharField(
        max_length=200,
        null=True,
        default='',
    )

    def __str__(self):
        return str(self.uuid)
    
    def get_email(self):
        return str(self.email)
    
    def validate(self,data):
        search_email=data.get('email',None)

        if User.objects.filter(email=search_email).exists():
            print('이미 있는 아이디입니다.')

        return data
