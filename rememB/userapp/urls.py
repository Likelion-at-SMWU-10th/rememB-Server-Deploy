from django.urls import path,include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('admin/',views.user_list,name='signin'), #유저 계정 전체 조회
    path('mypage/<uuid:pk>/',views.user_detail,name='user_detail'), #pk 계정 상세조회, 수정, 삭제
    path('signin/',views.JWTSigninView.as_view()), #jwt 로그인
    
    # token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), #username, password 필요
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), #access_token 재발급
	path('token/verify/', TokenVerifyView.as_view(), name='token_verify'), #token 유효성 검사
]
