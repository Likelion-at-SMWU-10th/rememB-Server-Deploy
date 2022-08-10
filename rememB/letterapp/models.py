from django.db import models
from userapp.models import User

class Letter(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    imgfolder_no=models.IntegerField(null=True)
    img_no = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    position_x = models.IntegerField(null=True)
    position_y = models.IntegerField(null=True)

    def __str__(self):
        return self.content[:7]
    
