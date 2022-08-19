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

    def __str__(self):
        return str(self.user)
