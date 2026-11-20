"""
URL configuration for bypc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from builder import views
from builder.admin import admin_site

urlpatterns = [
    path('', views.index, name='index'),
    path('api/builds/save/', views.save_build, name='save_build'),
    path('api/builds/list/', views.list_builds, name='list_builds'),
    path('api/builds/load/<int:bid>/', views.load_build, name='load_build'),
    path('api/builds/delete/<int:bid>/', views.delete_build, name='delete_build'),
    path('api/builds/clear/', views.clear_builds, name='clear_builds'),
    path('admin/', admin_site.urls),
]
