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
from django.urls import path
from builder import views
from bypc.admin_site import admin_site

urlpatterns = [
    path('', views.home, name='home'),
    # Tavsiya etilgan yo'llar (chiziqcha bilan) + siz so'ragan underscore ko'rinishidagi aliaslar
    path('pc-assembly/', views.pc_assembly, name='pc_assembly'),
    path('aio-assembly/', views.aio_assembly, name='aio_assembly'),
    path('pc_assembly/', views.pc_assembly),
    path('aio_assembly/', views.aio_assembly),
    path('monitors/', views.monitors, name='monitors'),
    path('printers/', views.printers, name='printers'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('cart/', views.cart_view, name='cart'),
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/export/', views.export_orders, name='export_orders'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/<int:pk>/edit/', views.order_edit, name='order_edit'),
    path('orders/<int:pk>/status/', views.order_status, name='order_status'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),
    # Eski havolalar ishlashda davom etadi
    path('seller/', views.seller_redirect, name='seller'),
    path('seller/orders/', views.orders_list),
    path('seller/orders/<int:pk>/', views.order_detail),
    path('seller/orders/<int:pk>/edit/', views.order_edit),
    path('seller/orders/<int:pk>/status/', views.order_status),
    path('seller/orders/<int:pk>/delete/', views.order_delete),
    path('seller/export/', views.export_orders),
    path('api/builds/save/', views.save_build, name='save_build'),
    path('api/builds/list/', views.list_builds, name='list_builds'),
    path('api/builds/load/<int:bid>/', views.load_build, name='load_build'),
    path('api/builds/delete/<int:bid>/', views.delete_build, name='delete_build'),
    path('api/builds/clear/', views.clear_builds, name='clear_builds'),
    path('admin/', admin_site.urls),
]
