from django.contrib.auth.base_user import AbstractBaseUser

from django.db import models

# Create your models here.
from django.db.models import SET_NULL


class User(AbstractBaseUser):
    phonenumber = models.CharField(max_length=100)
    code = models.CharField(max_length=5)

    def __str__(self):
        return self.phonenumber


class ConfirmationCode(models.Model):
    code = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True)
    valid_until = models.DateTimeField()

    def __str__(self):
        return self.code