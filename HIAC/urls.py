"""HICCAccountingProgram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

from . import views

app_name = 'HIAC'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('intro/', views.intro, name='intro'),
    path('account_setting/', views.account_setting, name='account_setting'),
    path('search_data/', views.search_data, name='search_data'),
    path('ok_button/', views.ok_button, name='ok_button'),
    path('download_button/', views.download_button, name='download_button'),
    path('donwload/', views.download, name='download'),
    path('upload_data/', views.upload_data, name='upload_data'),
    path('show_data/', views.show_data, name='show_data'),
    path('database_download/', views.database_download, name='database_download'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
