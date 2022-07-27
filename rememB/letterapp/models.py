from django.db import models

from userapp.models import User

class Letter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 유저와 연동
    letter_content = models.CharField(max_length=300)
    img_no = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    position_x = models.IntegerField()
    position_y = models.IntegerField()


