from rest_framework import serializers

from news.models import News, FavoriteNews
from users.serializers import UserSerializer


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = 'id title image description created link'.split()


class NewsCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=False)


class FavoriteNewsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    news = NewsSerializer()

    class Meta:
        model = FavoriteNews
        fields = 'id user news'.split()