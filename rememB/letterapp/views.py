from .serializers import *
from .models import Letter, User
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.shortcuts import get_object_or_404


class LetterSend(APIView):
    #userpk에게 편지 작성
    def post(self, request, userpk):
        user=get_object_or_404(User,pk=userpk)
        serializer=LetterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LetterList(APIView):
    #전체 편지 조회
    def get(self, request):
        letters=Letter.objects.all()
        serializer=LetterSerializer(letters, many=True)
        return Response(serializer.data)

class LetterUserList(APIView):
    #userpk의 편지만 조회
    def get(self,request,userpk):
        user_letters=Letter.objects.filter(user=userpk)
        serializer=LetterSerializer(user_letters, many=True)
        return Response(serializer.data)


class LetterDetail(APIView):
    def get_object(self, letterpk):
        try:
            return Letter.objects.get(pk=letterpk)
        except Letter.DoesNotExist:
            raise Http404
    
    def get(self, request, letterpk):
        letter=self.get_object(letterpk)
        serializer=LetterSerializer(letter)
        return Response(serializer.data)
    
    #기능 구현 필요없음
    def put(self, request, letterpk):
        letter=self.get_object(letterpk)
        serializer=LetterSerializer(letter,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #기능 구현 필요없음
    def delete(self, request, letterpk):
        letter=self.get_object(letterpk)
        letter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
