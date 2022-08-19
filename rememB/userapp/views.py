from rest_framework.response import Response
from .models import User
from .serializers import JWTSigninSerializer, UserSerializer
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from rest_framework import permissions
from .authenticate import SafeJWTAuthentication
import datetime


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
            serializers=MyUserSerializer(obj)
            return Response(serializers.data)
        return Response({"error":"User Perimition Denied"},status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, pk):
        #put: pk의 계정 정보 수정
        #필수 요청 항목: email, provider
        token_user=str(SafeJWTAuthentication.authenticate(self, request)[0])
        request_user=str(User.objects.filter(id=pk).values('email'))

        if token_user in request_user:
            obj=User.objects.get(id=pk)
            serializer=UserSerializer(obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error":"User Perimition Denied"},status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk):
        #delete: pk의 계정 정보 삭제
        token_user=str(SafeJWTAuthentication.authenticate(self, request)[0])
        request_user=str(User.objects.filter(id=pk).values('email'))

        if token_user in request_user:
            obj=self.get_object(pk)
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error":"User Perimition Denied"},status=status.HTTP_401_UNAUTHORIZED)


class JWTSigninView(generics.CreateAPIView):
    authentication_classes=[SafeJWTAuthentication]
    permission_classes=[permissions.AllowAny]

    serializer_class=JWTSigninSerializer

    def post(self,request):
        try:
            date_birth=request.data['birth']
            if len(date_birth)==4:
                month=int(date_birth[:2])
                day=int(date_birth[2:])
                date_birth=str(datetime.date(1000,month,day))
                request.data['birth']=date_birth
            
            user = User.objects.get_or_create( 
                email=request.data['email'],
                provider=request.data['provider'],
                #birth=request.data['birth'],
            )
        except:
            if User.objects.get(email=request.data['email']):
                data={
                    'error':'email account is exist. try other social auth!'
                }
                return Response(data, status=status.HTTP_409_CONFLICT)
            data = {
                    'error':'request data is wrong'
                }
            return Response(data, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get( 
                email=request.data['email'],
                provider=request.data['provider'],
            )
            user.last_login=timezone.now()
            user.username=request.data['username']
            user.birth=request.data['birth']
            try:
                user.background=request.data['background']
            except:
                pass
            try:
                user.text=request.data['text']
            except:
                pass
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
