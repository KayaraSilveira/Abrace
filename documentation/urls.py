from django.urls import path

from . import views

app_name = 'documentation'

urlpatterns = [
    path('', views.documentation, name='documentation'),
    path('routes/', views.documentation_routes, name='routes'),
]