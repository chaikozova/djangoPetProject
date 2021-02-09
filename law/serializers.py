from rest_framework import serializers

from law.models import Laws
from users.serializers import UserSerializer


class LawsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laws
        fields = 'id title description date file'.split()


class LawsCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=False)


class FavoriteLawsSerializer(serializers.ModelSerializer):
    user = UserSerializer
    laws = LawsSerializer
