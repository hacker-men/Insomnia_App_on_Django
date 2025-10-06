from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),  # Root for app
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sleep-history/', views.sleep_history, name='sleep_history'),
    # path('sleep-statistics/', views.sleep_statistics, name='sleep_statistics'),
    path('tips/', views.tips, name='tips'),
]