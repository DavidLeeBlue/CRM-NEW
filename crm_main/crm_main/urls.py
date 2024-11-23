
from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include
from core.views import index
from userprofile.views import signup

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('dashboard/leads/', include('lead.urls')),
    path('dashboard/clients/', include('client.urls')),
    path('dashboard/products/', include('product.urls')),
    path('dashboard/orders/', include('order.urls')),
    path('dashboard/ordersnew/', include('ordernew.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('dashboard/users/', include('userprofile.urls')),
    # path('sign-up/', signup, name='signup'),
    path('log-in/',views.LoginView.as_view(template_name='userprofile/login.html') ,name='login'),
    path('log-out/',views.LogoutView.as_view() ,name='logout'),
    # path('log-in/', views.LoginView.as_view(template_name='userprofile/login.html', authentication_form=LoginForm), name='login'),
    # path('log-out/', views.LogoutView.as_view(), name='logout'),
    # path('tickets/', include('tickets.urls')),
    path('tickets/', include('ticket.urls')),
  
]

"""
URL configuration for crm_main project.

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