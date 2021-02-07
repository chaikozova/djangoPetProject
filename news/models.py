import os

from django.db import models

# Create your models here.
from django.db.models import Model
from django.utils import timezone


def upload_to(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    milliseconds = now.milliseconds
    return f'users/{instance.pk}/{now:%Y%m%d%H%M%S}{milliseconds}{extension}'


class News(models.Model):
    class Meta:
        verbose_name = 'Новости'
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(null=True, upload_to='upload_to')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    link = models.TextField()

    def __str__(self):
        return self.title