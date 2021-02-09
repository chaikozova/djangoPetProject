from django.db import models

# Create your models here.
from users.models import User


class Publications(models.Model):
    class Meta:
        verbose_name = 'Публикации'
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(blank=True)

    def __str__(self):
        return self.title


class FavoritePublications(models.Model):
    publication = models.ForeignKey(Publications, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)