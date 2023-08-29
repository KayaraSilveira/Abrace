from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('project/new', views.ProjectDashboard.as_view(), name='project_new'),
    path('project/edit/<str:project_pk>', views.ProjectDashboard.as_view(), name='project_edit'), 
    path('project/detail/<str:project_pk>', views.ProjectDetail.as_view(), name='project_detail'),
    path('post/send', views.send_post, name='send_post'),
    path('comment/send', views.send_comment, name='send_comment'),
    path('post/detail/<str:post_pk>', views.PostDetail.as_view(), name='post_detail'),
]