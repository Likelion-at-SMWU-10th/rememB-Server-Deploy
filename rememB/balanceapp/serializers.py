from datetime import datetime
from rest_framework import serializers
from .models import *
from datetime import datetime
from userapp.models import User


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields='__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Answer
        fields='__all__'


class BalancePostSerializer(serializers.ModelSerializer):
    leftDay=serializers.SerializerMethodField()

    class Meta:
        model=Balance
        fields = (
            'user',
            'leftDay',
            'question_id',
            'answer_id',
        )
    
    def get_leftDay(self, obj):
        return User.getDayBefore(str(User.objects.get(id=obj.user.id).birth))


class BalanceSerializer(serializers.ModelSerializer):
    qcontent=serializers.SerializerMethodField()
    acontent1=serializers.SerializerMethodField()
    acontent2=serializers.SerializerMethodField()

    class Meta:
        model=Balance
        fields = (
            'user',
            'question_id',
            'answer_id',
            'qcontent',
            'acontent1',
            'acontent2'
        )

    #유효하지 않은 값이 들어왔을 때 오류처리해야함
    def get_qcontent(self, obj):
        return Question.objects.get(id=obj.question_id.id).question_content
    
    def get_acontent1(self, obj): 
        return Answer.objects.get(id=obj.question_id.id*2-1).answer_content
    
    def get_acontent2(self, obj): 
        return Answer.objects.get(id=obj.question_id.id*2).answer_content

#모든 질문과 답 보내는 api
class BAQSerializer(serializers.ModelSerializer):
    a1id=serializers.SerializerMethodField()
    a1content=serializers.SerializerMethodField()
    a2id=serializers.SerializerMethodField()
    a2content=serializers.SerializerMethodField()

    class Meta:
        model=Question
        fields = (
            'id',
            'question_content',
            'a1id',
            'a1content',
            'a2id',
            'a2content',
        )

    #유효하지 않은 값이 들어왔을 때 오류처리해야함
    def get_a1id(self, obj):
        return Answer.objects.get(id=(obj.id*2-1)).id
    
    def get_a1content(self, obj): 
        return Answer.objects.get(id=(obj.id*2-1)).answer_content
    
    def get_a2id(self, obj):
        return Answer.objects.get(id=(obj.id*2)).id
    
    def get_a2content(self, obj): 
        return Answer.objects.get(id=(obj.id*2)).answer_content