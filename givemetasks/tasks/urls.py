from django.urls import path
from .import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_task, name='add_task'),
    path('complete/<int:id>/', views.complete_task, name='complete'),
    path('delete/<int:id>/', views.delete_task, name='delete'),
    path('progress/', views.progress, name='progress'),
]