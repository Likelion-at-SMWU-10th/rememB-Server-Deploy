from django.db import models

from userapp.models import User

# Create your models here.
class Question(models.Model):
    question_content=models.CharField(max_length=300, null=False, blank=False,)

    def __str__(self):
        return str(self.question_content[:10])

class Answer(models.Model):
    answer_content=models.CharField(max_length=300, null=False, blank=False,)

    def __str__(self):
        return str(self.answer_content[:30])

class Balance(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True,)
    answer_id=models.ForeignKey(Answer, on_delete=models.CASCADE, null=True,)
    question_id=models.ForeignKey(Question, on_delete=models.CASCADE, null=True,)

# class QAContent(models.Model):
#     q_id=models.IntegerField() 
#     a1_id=models.IntegerField() 
#     a2_id=models.IntegerField()
#     q_content=models.CharField()
#     a1_content=models.CharField()
#     a2_content=models.CharField()