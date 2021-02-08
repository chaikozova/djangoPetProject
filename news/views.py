from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework import status, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from news.models import News, FavoriteNews
from news.permissions import IsClient
from news.serializers import NewsSerializer, NewsCreateSerializer, FavoriteNewsSerializer


class NewsAPIView(APIView, PageNumberPagination):
    allowed_methods = ['get', 'post']
    serializer_class = NewsSerializer

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query', '')
        news = News.objects.filter(Q(title__exact=query) |
                                   Q(description__contains=query))
        result = self.paginate_queryset(news, request, view=self)
        return self.get_paginated_response(self.serializer_class(result, many=True).data)

    def post(self, request, *args, **kwargs):
        serializer = NewsCreateSerializer(data=request.data)
        if serializer.is_valid():
            article = News.objects.create(title=serializer.title,
                                          description=serializer.description)
            article.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class NewsDetailView(APIView):
    allowed_methods = ['get','put', 'delete']
    serializer_class = NewsSerializer

    def get(self, request, id):
        news = News.objects.get(id=id)
        return Response(data=self.serializer_class(news, many=False).data)

    def put(self, request, id):
        news = News.get(id=id)
        title = request.data.get('title')
        description = request.data.get('description')
        news.title = title
        news.description = description
        news.save()

    def delete(self, request, id):
        news = News.objects.get(id=id)
        news.delete()
        news = News.objects.all()
        return Response(data=self.serializer_class(news, many=True).data)


class FavoriteCreateListDestroyApiView(APIView):
    permission_classes = [IsClient]

    def post(self, request):
        news_id = int(request.data.get('news_id'))
        try:
            favorite = FavoriteNews.objects.get(news_id=news_id,
                                                   user=request.user)
        except:
            favorite = FavoriteNews.objects.create(news_id=news_id,
                                                   user=request.user)
            favorite.save()
        return Response(status=status.HTTP_200_OK,
                        data=FavoriteNewsSerializer(favorite).data)

    def get(self, request):
        favorites = FavoriteNews.objects.filter(user=request.user)
        return Response(data=FavoriteNewsSerializer(favorites, many=True).data,
                        status=status.HTTP_200_OK)

    def delete(self, request):
        news_id = int(request.data.get('news_id'))
        favorites = FavoriteNews.objects.filter(news_id=news_id,
                                                user=request.user)
        favorites.delete()
        return Response(status=status.HTTP_200_OK)