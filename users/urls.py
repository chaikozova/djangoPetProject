from django.urls import path
from . import views as users

urlpatterns = [
    path('api/v1/register/', users.RegisterApiView.as_view()),
    path('api/v1/confirm/', users.ConfirmApiView.as_view()),
    path('api/v1/login/', users.LoginApiView.as_view()),
]