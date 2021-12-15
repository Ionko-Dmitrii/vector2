# Generated by Django 3.2.5 on 2021-08-27 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vector', '0003_delete_wallets'),
    ]

    operations = [
        migrations.CreateModel(
            name='wallets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet', models.TextField(null=True, verbose_name='Кошелек')),
                ('currency', models.TextField(null=True, verbose_name='Валюта')),
            ],
            options={
                'verbose_name': 'кошелек',
                'verbose_name_plural': 'кошельки',
                'db_table': 'wallets',
            },
        ),
    ]
