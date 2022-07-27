from django.db import models
from userapp.models import User

# Create your models here.
class Question(models.Model):
    question_content = models.CharField(max_length=200)

class Answer(models.Model):
    answer_content = models.CharField(max_length=200)

class Balance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 모델과 연동
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

