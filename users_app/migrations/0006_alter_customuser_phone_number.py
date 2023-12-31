# Generated by Django 4.2.8 on 2023-12-21 11:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0005_alter_customuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, validators=[django.core.validators.RegexValidator(message="Номер должен быть такого формата: '0xxxxxxxxx'.", regex='^\\0\\d{9}$')]),
        ),
    ]
