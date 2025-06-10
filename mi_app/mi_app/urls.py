
from django.contrib import admin
from django.urls import path,include
from account.views import user_login
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path ('', lambda request: redirect('login'))
]
