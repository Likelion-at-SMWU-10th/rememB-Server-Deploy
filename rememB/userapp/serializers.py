from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'


class JWTSigninSerializer(serializers.ModelSerializer):
    email=serializers.EmailField()
    username=serializers.CharField()
    provider=serializers.CharField(max_length=20)
    birth=serializers.DateField()
    
    class Meta:
        model=User
        fields='__all__'
