from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from law.models import Laws, FavoriteLaws
from law.serializers import LawsSerializer, LawsCreateSerializer, FavoriteLawsSerializer
from news.permissions import IsClient


class LawsApiView(APIView, PageNumberPagination):
    allowed_methods = ['get', 'post']
    serializer_class = LawsSerializer

    def get(self, request, *args, **kwargs):
        quary = request.query_params.get('quary', '')
        laws = Laws.objects.filter(Q(title__contains=quary) |
                                   Q(description__contains=quary))
        results = self.paginate_queryset(laws, request, view=self)
        return self.get_paginated_response(self.serializer_class(results, many=True).data)

    def post(self, request, *args, **kwargs):
        title = request.data.get('title')
        description = request.data.get('description')
        law = Laws.objects.create(title=title,
                                  description=description)
        law.save()
        return Response(data=self.serializer_class(law).data,
                        status=status.HTTP_201_CREATED)


class LawsDetailView(APIView):
    allowed_methods = ['get', 'put', 'delete']
    serializer_class = LawsSerializer

    def get(self, request, id):
        laws = Laws.objects.get(id=id)
        return Response(data=self.serializer_class(laws, many=False).data)

    def put(self, request, id):
        laws = Laws.objects.get(id=id)
        title = request.data.get('title')
        description = request.data.get('description')
        laws.title = title
        laws.description = description
        laws.save()

    def delete(self, request, id):
        laws = Laws.objects.get(id=id)
        laws.delete()
        laws = Laws.objects.all()
        return Response(data=self.serializer_class(laws, many=True).data)


class FavoriteLawsCreateAndDestroyApiView(APIView):
    permission_classes = [IsClient]

    def post(self, request):
        laws_id = int(request.data.get('laws_id'))
        try:
            favorite = FavoriteLaws.objects.get(laws_id=laws_id,
                                                user=request.users)
        except:
            favorite = FavoriteLaws.objects.create(laws_id=laws_id,
                                                   user=request.users)
            favorite.save()
        return Response(status=status.HTTP_200_OK,
                        data=FavoriteLawsSerializer(favorite).data)

    def get(self, request):
        favorites = FavoriteLaws.objects.filter(user=request.user)
        return Response(status=status.HTTP_200_OK,
                        data=FavoriteLawsSerializer(favorites, many=True).data)

    def delete(self, request):
        laws_id = int(request.data.get('laws_id'))
        favorites = FavoriteLaws.objects.filter(laws_id=laws_id,
                                                user=request.users)
        favorites.delete()
        return Response(status=status.HTTP_200_OK)
