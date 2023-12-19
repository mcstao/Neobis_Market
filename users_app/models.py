from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(unique=True, max_length=30)
    email = models.EmailField(unique=True, max_length=30)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    phone_regex = RegexValidator(
        regex=r'^\+996\d{9}$',
        message="Номер должен быть такого формата: '+996xxxxxxxxx'."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=13, unique=True, blank=True)
    profile_image = models.ImageField()


