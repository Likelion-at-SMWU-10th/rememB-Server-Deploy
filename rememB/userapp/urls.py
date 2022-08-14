from django.urls import path,include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('admin/',views.user_list.as_view()), #유저 계정 전체 조회
    path('mypage/<int:pk>/',views.user_detail.as_view()), #pk 계정 상세조회, 수정, 삭제
    path('signin/',views.JWTSigninView.as_view()), #jwt 로그인
    path('auth-test/',views.UserAuthTestView.as_view()), 
    
    #jwt token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), #post: access_token 재발급
]
