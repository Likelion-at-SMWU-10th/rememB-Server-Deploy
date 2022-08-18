from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions

from userapp.authenticate import SafeJWTAuthentication

from .models import Answer, Balance, Question
from .serializers import AnswerSerializer, BAQSerializer, BalancePostSerializer, QuestionSerializer, BalanceSerializer
from userapp.models import User


class QuestionList(APIView):
    authentication_classes=[SafeJWTAuthentication]
    permission_classes=[permissions.IsAdminUser]

    def get(self, request): #작성한 모든 질문 보기
        questions=Question.objects.all()
        serializers=QuestionSerializer(questions, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request): #질문 작성해서 DB에 저장
        serializer = QuestionSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswerList(APIView):
    authentication_classes=[SafeJWTAuthentication]
    permission_classes=[permissions.IsAdminUser]

    def get(self, request): #작성한 모든 답 보기
        answers=Answer.objects.all()
        serializers=AnswerSerializer(answers, many=True)
        return Response(serializers.data)
    
    def post(self, request): #답 작성해서 DB에 저장
        serializer = AnswerSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BalanceList(APIView): #user(pk)의 질문&대답 목록 
    authentication_classes=[SafeJWTAuthentication]
    permission_classes=[permissions.IsAdminUser]

    def get(self, request, pk): #한 유저의 전체 질문&대답 fk 전해주기
        balances=Balance.objects.filter(id=pk)
        serializers=BalanceSerializer(balances,many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

# balance/myist/<int:pk>/에서
# 1. 한 유저의 전체적인 질문 & 대답

# balance/game/<int:pk>/
# 1. 유저의 pk로 해당 유저를 찾고 생일을 알아낸다음 오늘 날짜랑 비교한다.
# 2. 7일 이내라면 해당 질문과 답을 보여준다. / 밀린 게 있을 수도 있으니 다수 가능
# 3. 해당 답을 받아온다.

#/balance/list/<유저pk>
class myBalanceList(APIView): #user(pk)의 질문&대답 목록 
    authentication_classes=[SafeJWTAuthentication]
    permission_classes=[permissions.AllowAny]

    def get(self, request, pk): 
        user=User.objects.get(id=pk)
        balances=Balance.objects.filter(user=user) 
        serializers=BalanceSerializer(balances,many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

#/balance/ans/<질문번호>(=남은날짜)
class myBalanceGame(APIView):
    authentication_classes=[SafeJWTAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def post(self, request, pk): #밸런스게임 질문-답 선택(질문 형식으로)
        userobj=User.objects.get(id=request.data['user'])
        leftDay=User.getDayBefore(str(userobj.birth))
        # print("D-DAY", leftDay)
        if(leftDay == pk): #오늘의 밸런스 게임
            try: #이미 했다면
                balanceobj = Balance.objects.filter(user=userobj).get(question_id=pk)
                return Response('이미 참여했습니다.', status=status.HTTP_200_OK)
            except Balance.DoesNotExist: #안했으면
                if((request.data['question_id']==str(pk)) & ( (request.data['answer_id']==str(pk*2-1)) | (request.data['answer_id']==str(pk*2)))):
                    serializer = BalancePostSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response('질문/응답 번호가 잘못되었습니다.',status=status.HTTP_200_OK )

        elif(leftDay < pk): #지난 밸런스게임
            try: #이미 했다면
                balanceobj = Balance.objects.filter(user=userobj).get(question_id=pk)
                return Response('이미 참여했습니다.', status=status.HTTP_200_OK)
            except Balance.DoesNotExist: #안했으면
                if((request.data['question_id']==str(pk)) & ( (request.data['answer_id']==str(pk*2-1)) | (request.data['answer_id']==str(pk*2)))):
                    serializer = BalancePostSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response('질문/응답 번호가 잘못되었습니다.',status=status.HTTP_200_OK )
        else:
            return Response("D-day 해당하지 않음", status=status.HTTP_200_OK)
