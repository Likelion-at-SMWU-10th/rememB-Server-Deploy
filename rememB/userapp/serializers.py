from pkg_resources import require
from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.settings import api_settings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'

class JWTSignupSerializer(serializers.ModelSerializer):
    #uuid=serializers.UUIDField()
    email=serializers.EmailField()
    username=serializers.CharField()
    provider=serializers.CharField()
    birth=serializers.DateField()

    class Meta(object):
        model=User
        fields='__all__'
    
    def validate(self,data):
        search_email=data.get('email',None)

        if User.objects.filter(email=search_email).exists():
            raise serializers.ValidationError('user already exists')

        return data
    
    def create(self, validated_data):
        user=User.objects.create(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            provider=self.validated_data['provider'],
            birth=self.validated_data['birth']
        )
        user.save()
        return user

class JWTSigninSerializer(serializers.ModelSerializer):
    email=serializers.EmailField()
    username=serializers.CharField()
    provider=serializers.CharField(max_length=20)
    birth=serializers.DateField()

    class Meta:
        model=User
        fields='__all__'
    
    def validate(self, data):
        search_email=data.get('email',None)
        search_provider=data.get('provider',None)

        if User.objects.filter(email=search_email).exists():
            user=User.objects.get(email=search_email)

            if user.provider != search_provider:
                raise serializers.ValidationError('social account incorrect')
        
        else:
            raise serializers.ValidationError('user account not exist')
        
        token = TokenObtainPairSerializer.get_token(user)
        data = {
            'user' : user.uuid,
            'refresh_token' : str(token),
            'access_token' : str(token.access_token)
        }
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

