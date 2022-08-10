from django.urls import path
from . import views

urlpatterns=[
    path('admin/',views.LetterList.as_view()), #전체 편지 조회
    path('<int:userpk>/send/',views.LetterSend.as_view()), #userpk에게 편지 작성
    path('<int:letterpk>/',views.LetterDetail.as_view()), #letterpk의 편지 디테일
    path('<int:userpk>/list/',views.LetterUserList.as_view()), #userpk의 편지만 조회
]
