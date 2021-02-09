from django.db import models

# Create your models here.
from users.models import User


class Laws(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    file = models.FileField()

    def __str__(self):
        return self.title


class FavoriteLaws(models.Model):
    news = models.ForeignKey(Laws, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)