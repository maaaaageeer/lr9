from django.urls import path

from api import views

urlpatterns = [
    path('auth/login/', views.login_view, name='login'),
    path('bonuses/', views.bonus_view, name='bonuses')
]