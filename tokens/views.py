import logging

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

from tokens.crypto.blockchain_provider import BlockchainProvider
from tokens.crypto.rinkeby_nft_contract_provider import RinkebyContractProvider
from tokens.models import Token
from RockNBlockTestTask.settings import CONFIG

logger = logging.getLogger('eventer')


def CreateToken(request) -> HttpResponse:
    logger.info('Handling request: method [tokens/create]')
    if request.method == 'POST':
        url = request.POST.get('media_url')
        owner = request.POST.get('owner')
        node = CONFIG['blockchain']['node_url']
        contract = CONFIG['blockchain']['contract_address']
        abi = CONFIG['blockchain']['contract_abi']
        chain = CONFIG['blockchain']['chain_id']
        wallet_secret_key = CONFIG['blockchain']['wallet_secret']

        msg = 'Rock N Block message'
        logger.info('Successfully request processed, response: {}'.format(token))
        return HttpResponse(token.__str__())


def ListTokens(request) -> HttpResponse:
    if request.method == 'GET':
        logger.info('Handling request: method [tokens/list]')
        tokens = Token.objects.all()
        logger.info('Successfully request processed, response: {}'.format(tokens.__str__()))
        return HttpResponse(tokens.__str__())
    else:
        raise PermissionDenied


def TokenTotalSupply(request) -> HttpResponse:
    if request.method == 'GET':
        logger.info('Handling request: method [tokens/total_supply]')
        node = CONFIG['blockchain']['node_url']
        contract = CONFIG['blockchain']['contract_address']
        abi = CONFIG['blockchain']['contract_abi']
        blockchain_provider = BlockchainProvider(node_address=node).provider
        supply = RinkebyContractProvider(
            provider=blockchain_provider,
            contract_abi=abi,
            contract_address=contract
        ).totalSupply()
        logger.info('Successfully request processed, response: {}'.format(supply))
        return HttpResponse('Total supply: {}'.format(supply))
    else:
        raise PermissionDenied
