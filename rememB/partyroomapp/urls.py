from django.urls import path
from . import views


urlpatterns = [
     path('<int:userpk>/',views.PartyroomList.as_view()), #partyroom내용 보내줌
]
