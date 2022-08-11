from django.urls import path
from . import views


urlpatterns = [
    path('api/question/', views.QuestionList.as_view(), name="api_question"), 
    path('api/answer/', views.AnswerList.as_view(), name="api_answer"),
    path('api/alllist/<int:pk>/', views.BalanceList.as_view(), name="api_balance_by_id"),
    path('mylist/<int:pk>/', views.myBalanceList.as_view(), name="mylist"),
    path('game/<int:pk>/', views.myBalanceGame.as_view(), name="game"),
]