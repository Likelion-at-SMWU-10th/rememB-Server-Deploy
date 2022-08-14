from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('balance/',include('balanceapp.urls')),
    path('letter/',include('letterapp.urls')),
    path('partyroom/',include('partyroomapp.urls')),
    path('user/',include('userapp.urls')),
]
