from django.urls import path
from . import views


urlpatterns = [
    path('question/admin/', views.QuestionList.as_view(), name="api_question"), 
    path('answer/admin/', views.AnswerList.as_view(), name="api_answer"),
    path('balance/<int:userpk>/admin/', views.BalanceList.as_view(), name="api_balance_by_id"),
    path('mylist/<int:userpk>/', views.myBalanceList.as_view(), name="mylist"),
    path('game/<int:qpk>/', views.myBalanceGame.as_view(), name="game"),
]