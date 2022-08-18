from django.urls import path
from . import views

urlpatterns = [
    path('<int:userpk>/',views.UserLetterView.as_view()), #userpk의 편지만 조회
    path('rollpaper/<int:userpk>/',views.UserRollView.as_view()),
]

