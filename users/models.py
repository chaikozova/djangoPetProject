from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager

from django.db import models

# Create your models here.
from django.db.models import SET_NULL


ADMIN = 1
CLIENT = 2
USER_TYPE = (
    (ADMIN, 'ADMIN'),
    (CLIENT, 'CLIENT'),
)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    user_type = models.IntegerField(choices=USER_TYPE,
                                    verbose_name='Тип пользователя', default=CLIENT)
    username = models.CharField('username', unique=True, max_length=100)
    email = models.EmailField('email', null=True, max_length=100)
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField(default=True)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


class ConfirmationCode(models.Model):
    code = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True)
    valid_until = models.DateTimeField()

    def __str__(self):
        return self.code