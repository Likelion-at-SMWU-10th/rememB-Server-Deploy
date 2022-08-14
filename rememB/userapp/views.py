import http
from rest_framework.response import Response
from .models import User
from .serializers import JWTSigninSerializer, UserSerializer
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from rest_framework import permissions
from .authenticate import SafeJWTAuthentication


class UserAuthTestView(APIView):
    authentication_classes=[SafeJWTAuthentication]

    def get(self, request):
        user=request.user
        print(f"user정보: {user}")
        if not user:
            return Response({"error": "접근 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"message": "accepted"})


class user_list(APIView):
    authentication_classes=[SafeJWTAuthentication]
    permission_classes=[permissions.AllowAny]
    #permission_classes=[permissions.IsAdminUser]

    def get(self, request):
        #get: 계정 전체 조회
        users=User.objects.all()
        serializers=UserSerializer(users,many=True)
        return Response(serializers.data)


class user_detail(APIView):
    authentication_classes=[SafeJWTAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request, pk):
        token_user=str(SafeJWTAuthentication.authenticate(self, request)[0])
        request_user=str(User.objects.filter(id=pk).values('email'))

        if token_user in request_user:
            obj=User.objects.get(id=pk)
            serializers=UserSerializer(obj)
            return Response(serializers.data)
        return Response({"error":"User Perimtion Denied"},status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        #put: pk의 계정 정보 수정
        token_user=str(SafeJWTAuthentication.authenticate(self, request)[0])
        request_user=str(User.objects.filter(id=pk).values('email'))

        if token_user in request_user:
            obj=User.objects.get(id=pk)
            serializer=UserSerializer(obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error":" User Perimtion Denied"},status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        #delete: pk의 계정 정보 삭제
        token_user=str(SafeJWTAuthentication.authenticate(self, request)[0])
        request_user=str(User.objects.filter(id=pk).values('email'))

        if token_user in request_user:
            obj=self.get_object(pk)
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error":"User Perimtion Denied"},status=status.HTTP_400_BAD_REQUEST)


class JWTSigninView(generics.CreateAPIView):
    authentication_classes=[SafeJWTAuthentication]
    permission_classes=[permissions.AllowAny]

    serializer_class=JWTSigninSerializer

    def post(self,request):
        try:
            user = User.objects.get_or_create( 
                email=request.data['email'],
                provider=request.data['provider'],
                birth=request.data['birth'],
                username=request.data['username']
            )
        except:
            data = {
                    "results": {
                        "msg": "social provider error",
                        "code": "E500"
                    }
                }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get( 
                email=request.data['email'],
                provider=request.data['provider'],
            )
            user.last_login=timezone.now()
            token = RefreshToken.for_user(user)
            user.refreshToken = str(token)
            user.save()
            data =  {
                "results": {
                    "id" : user.id,
                    "refreshToken" : user.refreshToken,
                    "accessToken" : str(token.access_token),
                }
            }
            return Response(data, status=status.HTTP_200_OK)
