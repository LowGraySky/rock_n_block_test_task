import json
import logging

from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from tokens.blockchain_provider import BlockchainProvider
from tokens.rinkeby_nft_contract_provider import RinkebyContractProvider
from tokens.models import Token
from tokens.serializers import CreateTokenQueryParamsSerializer, TokenSerializer

logger = logging.getLogger("eventer")


@extend_schema()
class CreateTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CreateTokenQueryParamsSerializer(data=request.data)

        if serializer.is_valid():
            hash = BlockchainProvider.generateRandomRaw()
            media_url = serializer.validated_data.get("media_url")
            owner = serializer.validated_data.get("owner")

            Token(unique_hash=hash, media_url=media_url, owner=owner).save()
            provider = BlockchainProvider()
            transaction = RinkebyContractProvider(provider=provider).mint(
                owner=owner, media_url=media_url, unique_hash=hash
            )

            tx_hash = json.loads(transaction).get("tx_hash")
            token = Token.objects.filter(unique_hash=hash)
            token.update(tx_hash=tx_hash)
            return Response(token)


@extend_schema()
class ListTokenView(generics.ListCreateAPIView):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = TokenSerializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema()
class TotalSupplyTokenView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        provider = BlockchainProvider()
        supply = RinkebyContractProvider(provider=provider).totalSupply()
        return Response(supply)
