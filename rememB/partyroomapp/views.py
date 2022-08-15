from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions

from userapp.authenticate import SafeJWTAuthentication

from .serializers import PartyroomSerializer
from letterapp.models import Letter

from userapp.models import User

class PartyroomList(APIView):
    authentication_classes=[SafeJWTAuthentication]
    permission_classes=[permissions.AllowAny]

    #userpk의 파티룸 내용 조회
    def get(self,request,userpk):
        try:
            obj=Letter.objects.filter(user=userpk)
            serializer=PartyroomSerializer(obj, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

