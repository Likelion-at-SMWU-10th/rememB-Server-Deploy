from userapp.models import User
from letterapp.models import Letter
from rest_framework.views import APIView
from rest_framework.response import Response
from letterapp.serializers import *
from userapp.models import User
from rest_framework import permissions

class UserLetterView(APIView):
    permission_classes=[permissions.AllowAny]

    #userpk의 편지만 조회
    def get(self,request,userpk):
        user=User.objects.get(id=userpk)
        leftDay=User.getDayBefore(str(user.birth))
        user_letters=Letter.objects.filter(user=userpk)
        serializer=LetterSumSerializer(user_letters, many=True)
        data={
            'username':user.username,
            'left_birth':leftDay,
            'letters':serializer.data
        }
        return Response(data)
