from telnetlib import STATUS
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from urllib3 import HTTPResponse
from .models import User
from .serializers import UserSerializer
from rest_framework.parsers import JSONParser

@csrf_exempt
def user_list(request):
    #get: 계정 전체 조회
    if request.method=='GET':
        query_set=User.objects.all()
        serializers=UserSerializer(query_set,many=True)
        return JsonResponse(serializers.data, safe=False)
    
    #post: 회원가입
    elif request.method=='POST':
        data=JSONParser().parse(request)
        serializers=UserSerializer(data=data)
        if serializers.is_valid():
            serializers.save()
            return JsonResponse(serializers.data, status=201)
        return JsonResponse(serializers.error, status=400)

@csrf_exempt
def user_detail(request,pk):
    obj=User.objects.get(uuid=pk)

    #get: uuid로 계정 조회
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
        return HTTPResponse(status=204)

@csrf_exempt
def login(request):
    #post: 로그인
    if request.method=='POST':
        data=JSONParser().parse(request)
        search_email=data['email']
        obj=User.objects.get(email=search_email)

        #if data['uuid']==str(obj.uuid):
        if data['provider']==obj.provider:
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)
