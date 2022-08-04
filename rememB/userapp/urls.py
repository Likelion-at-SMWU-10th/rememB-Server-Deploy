from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('admin/',views.user_list,name='signin'), #유저 계정 전체 조회
    path('mypage/<uuid:pk>/',views.user_detail,name='user_detail'), #pk 계정 상세조회, 수정, 삭제
    path('signin/',views.JWTSigninView.as_view()), #jwt 로그인
    path('signup/',views.JWTSignupView.as_view()), #jwt 회원가입
    path('hello/',views.HelloView.as_view()), #jwt토큰 인증 테스트 뷰

    #jwt token
    path('token/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/',TokenVerifyView.as_view(), name='token_verify'),
]
