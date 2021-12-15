# Generated by Django 3.2.5 on 2021-08-31 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vector', '0009_withdraw_bank'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commission',
            name='withdraw',
        ),
        migrations.AddField(
            model_name='commission',
            name='withdraw_sber',
            field=models.PositiveIntegerField(default=1, verbose_name='Комиссия вывода на сбер в %'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commission',
            name='withdraw_tink',
            field=models.PositiveIntegerField(default=2, verbose_name='Комиссия вывода на тинькофф в %'),
            preserve_default=False,
        ),
    ]