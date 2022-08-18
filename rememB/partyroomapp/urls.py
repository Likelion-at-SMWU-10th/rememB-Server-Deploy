from django.urls import path
from . import views

urlpatterns = [
    path('<int:userpk>/',views.UserLetterView.as_view()), #userpk의 편지만 조회
]

