from audioop import maxpp
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime


class UserManager(BaseUserManager):
    def create_user(self, email, username, provider, birth, refreshToken, password=None):

        user=self.model(
            email=self.normalize_email(email),
            username=username,
            provider=provider,
            birth=birth,
        )
        user.set_unusable_password()
        return user
    
    def create_superuser(self, email, username, provider, birth, refreshToken, password=None):
        user=self.model(
            email=self.normalize_email(email),
            username=username,
            provider=provider,
            birth=birth,
        )
        user.set_unusable_password()
        user.is_admin=True
        return user


class User(AbstractBaseUser):

    background=[
        ('lp','#FFEFF3'),
        ('p','#FFDDDD'),
        ('or','#FFEED9'),
        ('y','#FFF8CC'),
        ('g','#DEF0EB'),
        ('lb','#D8EEFF'),
        ('b','#E2E8FF'),
        ('pu','#EDE9FF')
    ]

    text=[
        ('lp','#FE4179'),
        ('p','#FF6161'),
        ('or','#FE7B1D'),
        ('y','#6C6C6C'),
        ('g','#42B494'),
        ('lb','#1786DB'),
        ('b','#3753C0'),
        ('pu','#7341C3')
    ]

    id = models.AutoField(primary_key=True,)
    email=models.EmailField(verbose_name=('email'), max_length=64, unique=True, null=False, blank=False,)
    username=models.CharField(max_length=30, null=False, blank=False,)
    provider=models.CharField(max_length=20, null=False, blank=False,)
    birth=models.DateField(blank=True,null=True)
    refreshToken=models.CharField(max_length=2000, null=True, default='',)
    password=models.CharField(null=True, max_length=100)
    background=models.CharField(choices=background,max_length=2, default='lp')
    text=models.CharField(choices=text,max_length=2,default="lp")

    # User 모델의 필수 field
    is_active = models.BooleanField(default=True)    
    is_admin = models.BooleanField(default=False)
    
    objects=UserManager()

    def __str__(self):
        return str(self.email)
    
    def get_id(self):
        return str(self.id)
    
    def validate(self,data):
        search_email=data.get('email',None)
        if User.objects.filter(email=search_email).exists():
            print('이미 있는 아이디입니다.')
        return data
    
    def getDayBefore(mybirthday):
        mybirthdayList = mybirthday.split("-")
        byear = int(mybirthdayList[0])
        bmonth = int(mybirthdayList[1])
        bday = int(mybirthdayList[2])
        
        nowList = str(datetime.now().date()).split("-")
        nyear=int(nowList[0])
        nmonth = int(nowList[1])
        nday= int(nowList[2])

        if(bmonth<nmonth | ((bmonth==nmonth) & (bday<nday))): #이미 생일이 지난경우
            dday = datetime(nyear+1, bmonth, bday).date()
            now = datetime.now().date()
            print(str(dday-now).split(",")[0].split(" ")[0])
            return int(str(dday-now).split(",")[0].split(" ")[0])
        else:
            dday = datetime(nyear, bmonth, bday).date()
            print(dday)
            now = datetime.now().date()
            diff = str(dday-now).split(",")[0].split(" ")[0]
            print(diff)
            if diff=='0:00:00': #생일 당일인 경우
                return 0
            return int(diff)

    @property
    def is_staff(self):
        return self.is_admin
