from django.contrib.auth import login
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView,
)
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from account.forms import RegistrationForm, LoginForm, CustomPasswordResetForm
from account.models import User


class UserLoginView(LoginView):
    """Endpoint для входа"""

    template_name = 'index.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        user = User.objects.get(email=email)
        login(self.request, user)

        return JsonResponse(
            dict(succes=True, message='Вы успешно вошли',
                 url=self.success_url), status=200
        )

    def form_invalid(self, form):
        messages = []
        for i in form.errors:
            messages.append([i, form.errors[i]])

        return JsonResponse(
            dict(succes=False, message=messages), status=400
        )


class UserLogoutView(LogoutView):
    template_name = 'partials/header.html'


class RegistrationView(CreateView):
    """Endpoint для регистрации пользователя"""

    template_name = 'components/modal-registration.html'
    form_class = RegistrationForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save(commit=False)
        User(
            email=form.cleaned_data['email'],
        )
        user.set_password(form.cleaned_data['password'])
        user.save()

        login(self.request, user)

        return JsonResponse(
            dict(succes=True, message='Вы успешно зарегистрировались',
                 url=self.success_url), status=200
        )

    def form_invalid(self, form):
        messages = []
        for i in form.errors:
            messages.append([i, form.errors[i]])

        return JsonResponse(
            dict(succes=False, message=messages), status=400
        )


class SendLinkForNewPasswordView(TemplateView):
    """Страница для отправки смс на емаил для смены пароля"""

    template_name = 'reset-password.html'


class SuccessNewPasswordView(TemplateView):
    """Страница об успехе отправки смс"""

    template_name = 'success-password.html'


class UserPasswordResetView(PasswordResetView):
    """Endpoint для отправки ссылки на емайл для смены пароля"""

    template_name = 'reset-password.html'
    success_url = reverse_lazy('send-link-success')
    form_class = CustomPasswordResetForm


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    """Endpoint сброса пароля"""

    template_name = 'new-password.html'
    success_url = reverse_lazy('home')
    post_reset_login = True
