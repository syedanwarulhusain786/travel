from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from django.utils.translation import gettext as _

urlpatterns = [


    path('', views.index, name="index"),

	path('signout/', views.logoutUser, name="signout"),


    
]
