from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from django.contrib.auth.views import LogoutView

urlpatterns = [

    path('profile/', views.Profile, name='profile'),
    path('profile/<int:pk>/info', views.profile_info, name='profile_info'),
    path('profile/<int:pk>/<str:name>/update', views.Profile_update, name='profile_update'),
    path('register/', views.Register, name='register'),
    path('login/', auth_view.LoginView.as_view(template_name='Users_action/login.html'), name='login'),
   
    path('logout/', LogoutView.as_view(template_name='Users_action/logout.html'), name='logout'),
   
   # path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('downloadResume/<int:pk>', views.download_resume, name='resume-download'),

    path('profile/project-details/<int:pk>/', views.Project_detail_view, name='project_detail'),
    path('profile/add-project-details/', views.AddProjectView.as_view(), name='project_new'),
    path('profile/<int:pk>/delete-project-details/', views.DeleteProjectView.as_view(), name='project_delete'),
    path('profile/<int:pk>/update-project-details/', views.UpdateProjectView.as_view(), name='project_update'),
    path('profile/<int:pk>/follow/', views.followUser, name='follow'),
    path('profile/<int:pk>/followers/', views.displayFollowers, name='followers'),
    path('profile/search/', views.wrapper, name='wrapper_search'),
    path('profile/search-result/', views.searchProfiles, name='resultProfile'),

    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='Users_action/password_reset.html'), name='password_reset'),
    path('password-reset-done/', auth_view.PasswordResetDoneView.as_view(template_name='Users_action/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='Users_action/password_reset_confirm.html'), name='password_reset_confirm'),

    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='Users_action/password_reset_complete.html'),
         name='password_reset_complete'),

    path('activate-account/<uidb64>/<token>', views.VerificationView.as_view(), name='activate'),

    path('send-email-all/', views.SendEmailToAll, name='send_email_all'),
    path('contact-us/', views.contact, name='contact_us'),
]
