from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .serializers import JWTSigninSerializer, UserSerializer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

class user_list(APIView):
    def get(self, request):
        #get: 계정 전체 조회
        users=User.objects.all()
        serializers=UserSerializer(users,many=True)
        return Response(serializers.data)


class user_detail(APIView):
    def get(self,request, pk):
        obj=User.objects.get(id=pk)
        serializers=UserSerializer(obj)
        return Response(serializers.data)

    def put(self, request, pk):
        #put: pk의 계정 정보 수정
        obj=User.objects.get(id=pk)
        serializer=UserSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        #delete: pk의 계정 정보 삭제
        obj=self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JWTSigninView(generics.CreateAPIView):
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


class AuthUserView(APIView):
    #커스텀한 user모델에 권한 설정을 안해서 그런 것 같다
    #첫번째 계정을 admin계정으로 인식 -> 토큰 인식 됨
    #permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    def get(self, request):
        user=request.user.username
        print(f"user정보: {user}") #첫번째 계정으로 로그인했을 때: admin으로 출력 / username 삭제: AnonymousUser으로 출력
        if not user:
            return Response({"error": "접근 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"message": "Accepted"})
