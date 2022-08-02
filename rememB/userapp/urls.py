from django.urls import path
from . import views

urlpatterns = [
    path('signin/',views.login,name='login'),
    path('signup/',views.user_list,name='signin'),
    path('mypage/<uuid:pk>/',views.user_detail,name='user_detail'),
]
