from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from account.models import User


class RegistrationForm(forms.ModelForm):
    """Форма для регистрации"""

    bool_field = forms.BooleanField(
        required=True, error_messages={'required': 'Примите условия соглашения!'}
    )
    password = forms.CharField(
        widget=forms.PasswordInput, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'bool_field')


class LoginForm(forms.Form):
    """Форма для входа"""

    email = forms.CharField()
    password = forms.CharField()

    class Meta:
        model = User
        fields = ('email', 'password')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        user = User.objects.filter(email=email).first()

        if not user:
            raise ValidationError(
                {"email": "Пользователя с таким email не существует!!"}
            )
        else:
            check_password = user.check_password(password)
            if not check_password:
                raise ValidationError(
                    {"password": "Пароль не подходит!!"}
                )

        return self.cleaned_data


class CustomPasswordResetForm(PasswordResetForm):
    """Форма для отправки ссылки на емайл для смены пароля"""

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email).exists()
        if not user:
            raise ValidationError('Почтовый ящик не зарегистрирован!!')

        return email
