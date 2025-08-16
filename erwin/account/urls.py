from django.urls import path

from . import views


urlpatterns = [

    path('register/', views.register, name='register'),

    #email verification URLs
    path('email-verification/<str:uidb64>/<str:token>/', views.email_verification, name='email-verification'),
    path('email-verification/sent/', views.email_verification_sent, name='email-verification-sent'),
    path('email-verification/success/', views.email_verification_success, name='email-verification-success'),
    path('email-verification/failed/', views.email_verification_failed, name='email-verification-failed'),

    
    # Add other URL patterns here
    # path('login/', views.login, name='login'),
    # path('logout/', views.logout, name='logout'),
    # path('profile/', views.profile, name='profile'),
    # path('password_change/', views.password_change, name='password_change'),
    # path('password_reset/', views.password_reset, name='password_reset'),
    # path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    # path('password_reset_confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    # path('password_reset_complete/', views.password_reset_complete, name='password_reset_complete'),
    # path('activate/<uidb64>/<token>/', views.activate, name='activate')   

]