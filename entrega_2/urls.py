"""
URL configuration for entrega_2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index, name='index'),
    path('consulta_1', views.consulta_1, name='consulta_1'),
    path('consulta_2', views.consulta_2, name='consulta_2'),
    path('consulta_3', views.consulta_3, name='consulta_3'),
    path('consulta_4', views.consulta_4, name='consulta_4'),
    path('consulta_5', views.consulta_5, name='consulta_5'),
    path('consulta_6', views.consulta_6, name='consulta_6'),
    path('consulta_7', views.consulta_7, name='consulta_7'),
    path('consulta_8', views.consulta_8, name='consulta_8'),
    path('consulta_9', views.consulta_9, name='consulta_9'),
    path('consulta_10', views.consulta_10, name='consulta_10'),
    path('consulta_general',views.consulta_general, name='consulta_general'),
]
