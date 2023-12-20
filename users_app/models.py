
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(unique=True, max_length=30)
    email = models.EmailField(unique=True, max_length=30)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_regex = RegexValidator(
        regex=r'^\0\d{9}$',
        message="Номер должен быть такого формата: '0xxxxxxxxx'."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=13, unique=True, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatar_pics/', blank=True, null=True)
    verify_code = models.CharField(max_length=4, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username





