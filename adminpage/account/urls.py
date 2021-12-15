from django.urls import path

from account.views import (
    UserLoginView, UserLogoutView, RegistrationView, SendLinkForNewPasswordView,
    UserPasswordResetView, UserPasswordResetConfirmView, SuccessNewPasswordView,
)

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('send-link/', SendLinkForNewPasswordView.as_view(), name='send-link'),
    path('password-reset/', UserPasswordResetView.as_view(), name='password-reset'),
    path('send-link-success/', SuccessNewPasswordView.as_view(), name='send-link-success'),
    path(
        'reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
]
