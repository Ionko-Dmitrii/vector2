from django import forms
from .models import admins
permissions_choices = [
    ('обмен', 'Обмен'),
    ('вывод', 'Вывод'),
    ('пополнение', 'Пополнение'),
    ('техподдержка', 'Техподдержка'),
    ('верификация', 'Верификация')
]
class adminsForm(forms.ModelForm):
    class Meta():
        model = admins
        fields = '__all__'
        exclude = []
        widgets={
            'permissions': forms.CheckboxSelectMultiple(
                choices=permissions_choices
            )
        }

class walletsForm(forms.ModelForm):
    class Meta():
        widgets={
            'currency':forms.RadioSelect(
                choices=
                [
                    ('BTC', 'BTC'),
                    ('RUB', 'RUB')
                ]
            )
        }