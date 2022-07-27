from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer): # 유저 추가
    class Meta:
        model = User
        fields = ('id', 'email', 'provider', 'user_name', 'birthday')

class UserFindSerializer(serializers.ModelSerializer): # 유저 추가
    class Meta:
        model = User
        fields = ('email', 'provider')
