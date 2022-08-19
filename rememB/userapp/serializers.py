from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'

class MyUserSerializer(serializers.ModelSerializer):
    month=serializers.SerializerMethodField()
    day=serializers.SerializerMethodField()

    class Meta:
        model=User
        fields= ('id', 'last_login', 'email' , 'username', 'provider', 'birth', 'refreshToken', 'password', 'is_active' ,'is_admin', 'month', 'day' )

    def get_month(self, obj):
        month = str(User.objects.get(id=obj.id).birth).split("-")[1]
        if(month[0] == '0'):
            month = month[1]
        return month

    def get_day(self, obj):
        return str(User.objects.get(id=obj.id).birth).split("-")[2]


class JWTSigninSerializer(serializers.ModelSerializer):
    email=serializers.EmailField()
    username=serializers.CharField()
    provider=serializers.CharField(max_length=20)
    birth=serializers.DateField()
    
    class Meta:
        model=User
        fields='__all__'
