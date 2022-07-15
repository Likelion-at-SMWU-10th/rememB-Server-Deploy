from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('balanceapp/',include('balanceapp.urls')),
    path('letterapp/',include('letterapp.urls')),
    path('mainapp/',include('mainapp.urls')),
    path('accounts/',include('allauth.urls')),
]
