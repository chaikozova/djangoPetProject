from django.urls import path
from . import views as law

urlpatterns = [
    path('api/v1/laws/', law.LawsApiView.as_view()),
    path('api/v1/laws/<int:id>', law.LawsDetailView.as_view()),
    path('api/v1/favorites_laws/', law.FavoriteLawsCreateAndDestroyApiView.as_view()),
]
