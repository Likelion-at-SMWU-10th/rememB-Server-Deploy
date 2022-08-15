from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions

from userapp.authenticate import SafeJWTAuthentication

from .models import Answer, Balance, Question
from .serializers import AnswerSerializer, BAQSerializer, QuestionSerializer, BalanceSerializer
from userapp.models import User

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
        print(str(dday-now).split(",")[0].split(" ")[0])
        return int(str(dday-now).split(",")[0].split(" ")[0])
    else:
        dday = datetime(2022, bmonth, bday).date()
        print(dday)
        now = datetime.now().date()
        diff = str(dday-now).split(",")[0].split(" ")[0]
        print(diff)
        return int(diff)


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

# balance/myist/<int:pk>/에서
# 1. 한 유저의 전체적인 질문 & 대답

# balance/game/<int:pk>/
# 1. 유저의 pk로 해당 유저를 찾고 생일을 알아낸다음 오늘 날짜랑 비교한다.
# 2. 7일 이내라면 해당 질문과 답을 보여준다. / 밀린 게 있을 수도 있으니 다수 가능
# 3. 해당 답을 받아온다.

#실제 프론트와 전달할 api
class myBalanceList(APIView): #user(pk)의 질문&대답 목록 
    authentication_classes=[SafeJWTAuthentication]
    permission_classes=[permissions.AllowAny]

    def get(self, request, pk): 
        user=User.objects.get(id=pk)
        balances=Balance.objects.filter(user=user) 
        serializers=BalanceSerializer(balances,many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

class myBalanceGame(APIView):
    authentication_classes=[SafeJWTAuthentication]
    permission_classes=[permissions.AllowAny]
    
    def post(self, request, pk): #밸런스게임 질문-답 선택(질문 형식으로)
        user=User.objects.get(id=pk)
        leftDay=getDayBefore(str(user.birth))
        print(request.data)
        if(leftDay <=7):
            request.data['user'] = user.id
            serializer = BalanceSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("아직 응답 못함", status=status.HTTP_200_OK)

        
    def get(self, request, pk): #밸런스게임 질문-답 선택할수있도록 
        user=User.objects.get(id=pk)
        leftDay=getDayBefore(str(user.birth))

        if(leftDay <= 7): #생일 비교해보고 7일 이내라면
            questions=Question.objects.filter(id__gt=(leftDay-1)) #쿼리셋
            print(questions)
            serializer = BAQSerializer(questions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            # if serializer.is_valid():
            #     return Response(serializer.data, status=status.HTTP_200_OK) #질문이랑 데이터가 전달됨 
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        else: #7일 이내가 아니라면 아직 답을 확인할 수 없음
            print("not yet")
            return Response("not yet", status=status.HTTP_200_OK)


