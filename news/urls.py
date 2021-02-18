from django.urls import path
from . import views as news


urlpatterns = [
    path('api/v1/news/', news.NewsAPIView.as_view()),
    path('api/v1/news/<int:id>/', news.NewsDetailView.as_view()),
    path('api/v1/favorites/', news.FavoriteCreateListDestroyApiView.as_view()),

]
