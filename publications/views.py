from django.db.models import Q

# Create your views here.
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from news.permissions import IsClient
from publications.models import Publications, FavoritePublications
from publications.serializers import PublicationSerializer, PublicationCreateSerializer, FavoritePublicationSerializer


class PublicationsApiView(APIView, PageNumberPagination):
    allowed_methods = ['get', 'post']
    serializer_class = PublicationSerializer

    def get(self, request, *args, **kwargs):
        quary = request.query_params.get('quary', '')
        publications = Publications.objects.filter(Q(title__contains=quary) |
                                                   Q(description__contains=quary))
        results = self.paginate_queryset(publications, request, view=self)
        return self.get_paginated_response(self.serializer_class(results, many=True).data)

    def post(self, request, *args, **kwargs):
        serializer = PublicationCreateSerializer
        if serializer.is_valid():
            publication = Publications.objects.create(title=serializer.title,
                                                      description=serializer.description)
            publication.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class PublicationsDetailView(APIView):
    allowed_methods = ['get', 'put', 'delete']
    serializer_class = PublicationSerializer

    def get(self, request, id):
        publications = Publications.objects.get(id=id)
        return Response(data=self.serializer_class(publications, many=False).data)

    def put(self, request, id):
        publications = Publications.objects.get(id=id)
        title = request.data.get('title')
        description = request.data.get('description')
        publications.title = title
        publications.description = description
        publications.save()

    def delete(self, request, id):
        publications = Publications.objects.get(id=id)
        publications.delete()
        publications = Publications.objects.all()
        return Response(data=self.serializer_class(publications, many=True).data)


class FavoritePublicationCreateAndDestroyApiView(APIView):
    permission_classes = [IsClient]

    def post(self, request):
        publications_id = int(request.data.get('publications_id'))
        try:
            favorite = FavoritePublications.objects.get(publications_id=publications_id,
                                                        user=request.users)
        except:
            favorite = FavoritePublications.objects.create(publications_id=publications_id,
                                                           user=request.users)
            favorite.save()
        return Response(status=status.HTTP_200_OK,
                        data=FavoritePublicationSerializer(favorite).data)

    def get(self,request):
        favorites = FavoritePublications.objects.filter(user=request.user)
        return Response(status=status.HTTP_200_OK,
                        data=FavoritePublicationSerializer(favorites, many=True).data)

    def delete(self,request):
        publications_id = int(request.data.get('publications_id'))
        favorites = FavoritePublications.objects.filter(publications_id=publications_id,
                                                        user=request.users)
        favorites.delete()
        return Response(status=status.HTTP_200_OK)