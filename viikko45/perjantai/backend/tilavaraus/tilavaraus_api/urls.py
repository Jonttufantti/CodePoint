"""
URL configuration for tilavaraus_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from tilavaraus.views import kayttaja_list, kayttaja_detail, tilat_list, tilat_detail, varaajat_list, varaajat_detail, varaukset_list, varaukset_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('kayttajat/', kayttaja_list),
    path('kayttajat/<int:pk>/', kayttaja_detail),
    path('tilat/', tilat_list),
    path('tilat/<int:pk>/', tilat_detail),
    path('varaajat/', varaajat_list),
    path('varaajat/<int:pk>/', varaajat_detail),
    path('varaukset/', varaukset_list),
    path('varaukset/<int:pk>/', varaukset_detail),
]