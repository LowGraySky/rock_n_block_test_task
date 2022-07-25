from rest_framework import serializers

from tokens.models import Token


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = "__all__"


class CreateTokenQueryParamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ["media_url", "owner"]
