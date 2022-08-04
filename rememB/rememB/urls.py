from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from userapp import views

router=routers.DefaultRouter()
router.register('user',views.UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('balanceapp/',include('balanceapp.urls')),
    path('letterapp/',include('letterapp.urls')),
    path('mainapp/',include('mainapp.urls')),
    path('user/',include('userapp.urls')),
    path('auth', include('rest_framework.urls', namespace='rest_framework')),
    path('',include(router.urls)),
]
