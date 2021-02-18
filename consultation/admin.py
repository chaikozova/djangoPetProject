from django.contrib import admin

# Register your models here.
from consultation.models import UserQuestions, AdminAnswers

admin.site.register(UserQuestions)
admin.site.register(AdminAnswers)