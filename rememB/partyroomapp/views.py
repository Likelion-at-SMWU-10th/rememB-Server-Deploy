from userapp.models import User
from letterapp.models import Letter
from rest_framework.views import APIView
from rest_framework.response import Response
from letterapp.serializers import *
from userapp.models import User
from rest_framework import permissions, status
from userapp.authenticate import SafeJWTAuthentication


class UserLetterView(APIView):
    permission_classes=[permissions.AllowAny]

    #userpk의 편지만 조회
    def get(self,request,userpk):
        user=User.objects.get(id=userpk)
        leftDay=User.getDayBefore(str(user.birth))
        user_letters=Letter.objects.filter(user=userpk)
        serializer=LetterSumSerializer(user_letters, many=True)

        try:
            token_user=str(SafeJWTAuthentication.authenticate(self, request)[0])
            request_user=str(User.objects.filter(id=userpk).values('email'))
        except TypeError:
            data={
                'is_myparty':False,
                'username':user.username,
                'background':user.get_background_display(),
                'text':user.get_text_display(),
                'left_birth':leftDay,
                'letters':serializer.data
        }
        else:
            if token_user in request_user:
                data={
                'is_myparty':True,
                'username':user.username,
                'background':user.get_background_display(),
                'text':user.get_text_display(),
                'left_birth':leftDay,
                'letters':serializer.data
                }
            else:
                data={
                    'is_myparty':False,
                    'username':user.username,
                    'background':user.get_background_display(),
                    'text':user.get_text_display(),
                    'left_birth':leftDay,
                    'letters':serializer.data
                }
        return Response(data)


class UserRollView(APIView):
    authentication_classes=[SafeJWTAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self, request, userpk):
        token_user=str(SafeJWTAuthentication.authenticate(self, request)[0])
        request_user=str(User.objects.filter(id=userpk).values('email'))

        if token_user in request_user:
            user=User.objects.get(id=userpk)
            user_letters=Letter.objects.filter(user=userpk)
            serializer=LetterDetailSerializer(user_letters, many=True)
            data={
                'username':user.username,
                'background':user.get_background_display(),
                'text':user.get_text_display(),
                'letters':serializer.data
            }
            return Response(data)
        return Response({"error":"User Perimition Denied"},status=status.HTTP_401_UNAUTHORIZED)
