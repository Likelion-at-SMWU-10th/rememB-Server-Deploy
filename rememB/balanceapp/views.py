from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Answer, Balance, Question
from .serializers import AnswerSerializer, QuestionSerializer, BalanceSerializer
from userapp.models import User

# balance/myist/<int:pk>/에서
# 1. 한 유저의 전체적인 질문 & 대답(유저가 새로 로그인했을 때 만들어지는 것)

# balance/game/<int:pk>/
# 1. 유저의 pk로 해당 유저를 찾고 생일을 알아낸다음 오늘 날짜랑 비교한다.
# 2. 7일 이내라면 해당 질문과 답을 보여준다. / 밀린 게 있을 수도 있으니 다수 가능
# 3. 해당 답을 받아온다.

# balance/<int:pk>/
# 1. balance 모델에서 해당 유저 아이디로 검색하고, 답이 null값이 아니라면
# 2. 질문과 답을 api로 보여준다.

class QuestionList(APIView):
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
    def get(self, request, pk): #한 유저의 전체 질문&대답 fk 전해주기
        balances=Balance.objects.filter(id=pk)
        serializers=BalanceSerializer(balances,many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


#실제 프론트와 전달할 api
class myBalanceList(APIView): #user(pk)의 질문&대답 목록 
    
    def get(self, request, pk): 
        user=User.objects.get(id=pk)
        leftDay=getDayBefore(str(user.birth))

        balances=Balance.objects.filter(id=pk) 
        serializers=BalanceSerializer(balances,many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

def getDayBefore(mybirthday):
    mybirthdayList = mybirthday.split("-")
    byear = int(mybirthdayList[0])
    bmonth = int(mybirthdayList[1])
    bday = int(mybirthdayList[2])
    
    nowList = str(datetime.now().date()).split("-")
    nmonth = int(nowList[1])
    nday= int(nowList[2])

    if(bmonth<nmonth | ((bmonth==nmonth) & (bday<nday))): #이미 생일이 지난경우
        dday = datetime(2023, bmonth, bday).date()
        now = datetime.now().date()
        return str(dday-now).split(",")[0]
    else:
        dday = datetime(2022, bmonth, bday).date()
        print(dday)
        now = datetime.now().date()
        
        return str(dday-now).split(",")[0]
