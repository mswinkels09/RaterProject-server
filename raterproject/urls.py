"""raterproject URL Configuration

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
from gamerraterapi.views.game import Games
from django.conf.urls import include
from django.urls import path
from gamerraterapi.views import register_user, login_user

from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
#(r=patternmatch'what string client is looking for'
# Class that you are looking for, 
# 'descriptive name')
router.register(r'games', Games, 'game')

urlpatterns = [
    path('', include(router.urls)),
    #http://localhost:8000/register
    path('register', register_user),
    #http://localhost:8000/login
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('', include('gamerraterreports.urls')),
]
