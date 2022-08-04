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

class JWTSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = JWTSignupSerializer


class JWTSigninView(generics.CreateAPIView):
    serializer_class=JWTSigninSerializer

    def post(self,request):
        serializer=self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        token=serializer.validated_data
        return Response({"token":token}, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



