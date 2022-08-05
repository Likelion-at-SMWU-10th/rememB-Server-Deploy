from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .serializers import JWTSigninSerializer, UserSerializer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import generics, status
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets


@csrf_exempt
def user_list(request):
    #get: 계정 전체 조회
    if request.method=='GET':
        query_set=User.objects.all()
        serializers=UserSerializer(query_set,many=True)
        return JsonResponse(serializers.data, safe=False)

@csrf_exempt
def user_detail(request,pk):
    obj=User.objects.get(uuid=pk)

    #get: pk의 계정 조회
    if request.method=='GET':
        serializers=UserSerializer(obj)
        return JsonResponse(serializers.data, safe=False)
    
    #put: pk의 계정 정보 수정
    elif request.method=='PUT':
        data=JSONParser().parse(request)
        serializers=UserSerializer(obj, data=data)
        if serializers.is_valid():
            serializers.save()
            return JsonResponse(serializers.data, status=201)
        return JsonResponse(serializers.errors, status=400)

    #delete: pk의 계정 정보 삭제
    elif request.method=='DELETE':
        obj.delete()
        return HttpResponse(status=204)


class JWTSigninView(generics.CreateAPIView):
    serializer_class=JWTSigninSerializer

    def post(self,request):
        user = User.objects.get_or_create( 
            email=request.data['email'],
            provider=request.data['provider'],
            birth=request.data['birth'],
            username=request.data['username']
        )

        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
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
                        "uuid" : user.uuid,
                        "refreshToken" : user.refreshToken,
                        "accessToken" : str(token.access_token),
                    }
                }
                return Response(data=data, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                data = {
                    "results": {
                        "msg": "유저 정보가 올바르지 않습니다.",
                        "code": "E4010"
                    }
                }
                return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

            except Exception as e:
                print(e)
                data = {
                    "results": {
                        "msg": "정상적인 접근이 아닙니다.",
                        "code": "E5000"
                    }
                } 
                return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            data={
                "results":{
                    "error" : "serializer.is_valid() 에러",
                }
            }
            return Response(data=data, sstatus=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



