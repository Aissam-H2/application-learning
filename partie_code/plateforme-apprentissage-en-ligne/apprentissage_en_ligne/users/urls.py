from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # register
    path('register/',                        views.RegisterView.as_view(),       name='register'),

    # email verification
    path('verify-email/<uuid:token>/',       views.VerifyEmailView.as_view(),    name='verify-email'),

    # login / logout
    path('login/',                           views.LoginView.as_view(),          name='login'),
    path('logout/',                          views.LogoutView.as_view(),         name='logout'),

    # token refresh
    path('token/refresh/',                   TokenRefreshView.as_view(),         name='token-refresh'),

    # profile
    path('profile/',                         views.ProfileView.as_view(),        name='profile'),

    # password reset
    path('forgot-password/',                 views.ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/<uuid:token>/',     views.ResetPasswordView.as_view(),  name='reset-password'),
]