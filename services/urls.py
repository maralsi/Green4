from django.urls import path
from services import views

from experts import admin

urlpatterns = [
    path('', views.service_list_api_view),
    path('<int:id>/', views.service_detail_api_view)
]