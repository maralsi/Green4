"""
URL configuration for Green4 project.

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
from django.urls import path, include

from services import views
from experts import views
from reports import views
from rest_framework.routers import DefaultRouter

from . import swagger

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/services/', include('services.urls')),  # GET - List, Post - create
    path('api/v1/services/<int:id>/', views.service_detail_api_view),  # GET - item, PUT - update, DELETE - destroy
    path('api/v1/reports/', views.report_list_api_view),
    path('api/v1/reports/<int:id>/', views.report_list_api_view),
    path('api/v1/experts/', views.expert_list_api_view),
    path('api/v1/experts/<int:id>/', views.expert_detail_api_view),
    path('api/v1/reports/feedback/', views.report_feedback_api_view),
    path('api/v1/users', include('users.urls'))
]

urlpatterns += swagger.urlpatterns
