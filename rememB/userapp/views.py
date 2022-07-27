from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets

from .serializers import UserFindSerializer, UserSerializer
from .models import User
from .tokens import *

# Create your views here.
class UserList(APIView):
    def post(self, request): # 회원 등록하는 경우
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request): # 회원 조회하는 경우
        users = User.objects.all()
        serializer = UserSerializer(users, many=True) # 다수의 쿼리셋 전달 위해서 many = True
        return Response(serializer.data)

class UserFind(APIView):
    def post(self, request):
        serializer = UserFindSerializer(data = request.data)
        if serializer.is_valid():
            email = request.data['email']
            provider = request.data['provider']
            try:
                user = User.objects.get( 
                    email=email,
                    provider=provider
                )
                print(user.id)
                # payload에 넣을 값 커스텀 가능
                payload_value = user.id
                payload = {
                    "subject": payload_value,
                }

                access_token = generate_token(payload, "access")

                data = {
                    "results": {
                        "access_token": access_token
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

        

class AuthViewSet(viewsets.GenericViewSet):
    @action(methods=['POST'], detail=False)
    def signin(self, request):
        email = request.data['email']
        provider = request.data['provider']
        print(email, provider)
        try:
            user = User.objects.get( 
                email=email,
                provider=provider
            )
			
            # payload에 넣을 값 커스텀 가능
            payload_value = user.id
            payload = {
                "subject": payload_value,
            }

            access_token = generate_token(payload, "access")

            data = {
                "results": {
                    "access_token": access_token
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

def login(request):
    return render(request,'userapp/login.html')