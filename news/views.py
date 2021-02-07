from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework import status, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from news.models import News
from news.serializers import NewsSerializer, NewsCreateSerializer


class NewsAPIView(APIView, PageNumberPagination):
    allowed_methods = ['get', 'post']
    serializer_class = NewsSerializer

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query', '')
        news = News.objects.filter(Q(title_contains=query),
                                   Q(description_contains=query))
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