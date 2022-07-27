from django.db import models

# Create your models here.
class User(models.Model):
    email = models.CharField(max_length=100)
    provider = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    birthday = models.DateField()
    access_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    expire = models.CharField(max_length=100)
