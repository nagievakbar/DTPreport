"""DTPreport URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from DTPreport import settings
from makereport.views import user_login, user_logout, users_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('report/', include('makereport.urls')),
    path('',user_login, name='user_login'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('users/', users_list, name='users_list'),
    path('pdf/', include('pdf_report.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)