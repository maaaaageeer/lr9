from django.contrib import admin
from django.urls import path, include

from bonus_service import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]