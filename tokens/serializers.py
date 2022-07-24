from rest_framework import serializers

from tokens.models import Token


class CreateTokenQueryParamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ["media_url ", "owner "]
