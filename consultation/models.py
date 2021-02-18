from django.db import models

# Create your models here.
from users.models import User


class UserQuestions(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField()

    def __str__(self):
        return self.text

    def answer_view(self):
        return AdminAnswers.objects.filter(text=self)


class AdminAnswers(models.Model):
    question = models.ForeignKey(UserQuestions, on_delete=models.SET_NULL, null=True, related_name='answers')
    text = models.TextField()

    def __str__(self):
        return self.text