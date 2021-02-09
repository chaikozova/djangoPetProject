from rest_framework import serializers

from publications.models import Publications, FavoritePublications
from users.serializers import UserSerializer


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publications
        fields = 'id title description date file'.split()


class PublicationCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=False)


class FavoritePublicationSerializer(serializers.ModelSerializer):
    user = UserSerializer
    publication = PublicationSerializer

    class Meta:
        model = FavoritePublications
        fields = 'id user publications'.split()