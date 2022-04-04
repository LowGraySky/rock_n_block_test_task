import logging

from django.http import HttpResponse

from tokens.crypto.rinkeby_nft_contract_provider import RinkebyContractProvider
from tokens.models import Token
from RockNBlockTestTask.settings import CONFIG

logger = logging.getLogger('tokens_logger')


def CreateToken(reqeust, **kwargs) -> HttpResponse:
    logger.info('Handling request: method [tokens/create] with params: [{}][{}]'.format(*args, **kwargs))
    media_url = reqeust.data.get('media_url')
    owner = reqeust.data.get('owner')
    node = CONFIG['blockchain']['node_url']
    contract = CONFIG['blockchain']['contract_address']
    abi = CONFIG['blockchain']['contract_abi']
    token = Token(

    )
    logger.info('Successfully request processed, response: {}'.format(token))
    return HttpResponse(token.__str__())


def ListTokens(request, *args, **kwargs) -> HttpResponse:
    logger.info('Handling request: method [tokens/list]  with params: [{}][{}]'.format(*args, **kwargs))
    tokens = Token.objects.all()
    logger.info('Successfully request processed, response: {}'.format(tokens.__str__()))
    return HttpResponse(tokens.__str__())


def TokenTotalSupply(request) -> HttpResponse:
    logger.info('Handling request: method [tokens/total_supply]')
    node = CONFIG['blockchain']['node_url']
    contract = CONFIG['blockchain']['contract_address']
    abi = CONFIG['blockchain']['contract_abi']
    supply = None
    logger.info('Successfully request processed, response: {}'.format(supply))
    return HttpResponse('Total supply: {}'.format(supply))
