"""Search_module URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from parsers import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('queries_list/', views.QueryListView.as_view(), name='queries_list'),
    path('login/', views.LoginFormView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterFormView.as_view(), name='register'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('query_detail/<slug:slug>/', views.UserQueryDetail.as_view(), name='query_detail'),
    path('', views.new_query, name='new_query'),
    path('dash/', views.Dash.as_view(), name='dash')
]
