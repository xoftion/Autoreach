from django.urls import path
from . import views

urlpatterns = [
    path('', views.campaign_list, name='campaign_list'),
    path('create/', views.campaign_create, name='campaign_create'),
    path('<uuid:pk>/', views.campaign_detail, name='campaign_detail'),
    path('<uuid:pk>/start/', views.campaign_start, name='campaign_start'),
    path('track/<uuid:log_id>/', views.track_open, name='track_open'),
]
