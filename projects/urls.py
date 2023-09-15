from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.ProjectsList.as_view(), name='projects'),
    path('project/new', views.ProjectDashboard.as_view(), name='project_new'),
    path('project/edit/<str:project_pk>', views.ProjectDashboard.as_view(), name='project_edit'), 
    path('project/detail/<str:project_pk>', views.ProjectDetail.as_view(), name='project_detail'),
    path('post/send', views.send_post, name='send_post'),
    path('comment/send', views.send_comment, name='send_comment'),
    path('post/detail/<str:post_pk>', views.PostDetail.as_view(), name='post_detail'),
    path('project/enter', views.enter_project, name='project_enter'),
    path('project/leave', views.leave_project, name='project_leave'),
    path('project/delete', views.delete_project, name='project_delete'),
    path('project/members/<str:project_pk>', views.MembersList.as_view(), name='members_list'),
    path('project/mod/add', views.add_mod, name='mod_add'),
    path('project/mod/remove', views.remove_mod, name='mod_remove'),
]