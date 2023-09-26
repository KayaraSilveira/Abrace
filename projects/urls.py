from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.ProjectsList.as_view(), name='projects'),
    path('filter/category/<str:category>/', views.ProjectsList.as_view(), name='projects_filter'),
    path('project/new', views.ProjectDashboard.as_view(), name='project_new'),
    path('project/edit/categories/set/<str:project_pk>', views.set_categories, name='set_categories'),
    path('project/edit/categories/<str:project_pk>', views.save_categories, name='save_categories'),
    path('project/edit/<str:project_pk>', views.ProjectDashboard.as_view(), name='project_edit'), 
    path('project/detail/<str:project_pk>', views.ProjectDetail.as_view(), name='project_detail'),
    path('project/post/send', views.send_post, name='send_post'),
    path('project/comment/send', views.send_comment, name='send_comment'),
    path('project/post/detail/<str:post_pk>', views.PostDetail.as_view(), name='post_detail'),
    path('project/leave', views.leave_project, name='project_leave'),
    path('project/delete', views.delete_project, name='project_delete'),
    path('project/members/<str:project_pk>', views.MembersList.as_view(), name='members_list'),
    path('project/mod/add', views.add_mod, name='mod_add'),
    path('project/mod/remove', views.remove_mod, name='mod_remove'),
    path('project/member/remove', views.remove_member, name='member_remove'),
    path('project/post/delete', views.delete_post, name='post_delete'),
    path('project/solicitation/add', views.add_solicitation, name='solicitation_add'),
    path('project/solicitation/remove', views.remove_solicitation, name='solicitation_remove'),
    path('project/solicitation/accept', views.accept_solicitation, name='solicitation_accept'),
    path('project/solicitation/reject', views.reject_solicitation, name='solicitation_reject'),
    path('project/solicitation/<str:project_pk>', views.Solicitation.as_view(), name='project_solicitation'),
    path('project/deactivate/<str:project_pk>', views.deactivate, name='deactivate'),
    path('project/search/', views.search_project, name='search_project'),
]