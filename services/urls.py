from django.urls import path
from services import views

from experts import admin

urlpatterns = [
    path('', views.ServiceListAPIView.as_view()),
    path('<int:id>/', views.service_detail_api_view),
    path('categories/', views.CategoryListAPIView.as_view()),
    path('categories/<int:id>/', views.CategoryDetailAPIView.as_view()),
    path('tags/', views.TagViewSet.as_view({
        'get': 'list', 'post': 'create'
    })),
    path('tags/<int:id>/', views.TagViewSet.as_view({
            'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
    }))
]