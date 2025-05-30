
from django.contrib import admin
from django.urls import path
from account.views import user_login
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', user_login, name='login'),
    path ('', lambda request: redirect('login'))
]
