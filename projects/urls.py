from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('project/new', views.ProjectDashboard.as_view(), name='project_new'),
    path('project/edit/<str:project_pk>', views.ProjectDashboard.as_view(), name='project_edit'), 
]