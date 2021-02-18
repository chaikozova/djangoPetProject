from django.urls import path
from . import views as publications

urlpatterns = [
    path('api/v1/publications/', publications.PublicationsApiView.as_view()),
    path('api/v1/publications/<int:id>', publications.PublicationsDetailView.as_view()),
    path('api/v1/favorites_publications/', publications.FavoritePublicationCreateAndDestroyApiView.as_view()),
]