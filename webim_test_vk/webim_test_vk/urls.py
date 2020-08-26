from django.contrib import admin
from django.urls import include, path

from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
    path('', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
]
