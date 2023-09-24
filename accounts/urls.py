from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create', views.register_create, name='register_create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout', views.logout_view, name='logout'),
    path('profile/', views.ProfileDetail.as_view(), name='profile'),
    path('profile/edit', views.ProfileEdit.as_view(), name='profile_edit'),
    path('profile/edit/categories', views.save_categories, name='save_categories'),
    path('profile/projects', views.MyProjectsList.as_view(), name='my_projects'),
    path('profile/reviews', views.review_view, name='profile_reviews'),
    path('profile/view/<str:cpf>/', views.ViewProfile.as_view(), name='view_profile'),
    path('profile/view/<str:cpf>/reviews/', views.view_profile_review, name='view_profile_reviews'),
    path('profile/view/<str:cpf>/projects/', views.ViewProfileProjects.as_view(), name='view_profile_projects'),
    path('profile/view/<str:cpf>/projects/filter/<str:role>/', views.ViewProfileProjects.as_view(), name='view_profile_projects_filter'),
    path('review/<str:reviewed_pk>/<str:project_pk>', views.ReviewCreateView.as_view(), name='review'),
    path('profile/projects/filter/<str:role>/', views.MyProjectsList.as_view(), name='my_projects_filter'),
]
