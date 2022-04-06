import json
import logging

import web3.exceptions
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse

from tokens.crypto.blockchain_provider import BlockchainProvider
from tokens.crypto.rinkeby_nft_contract_provider import RinkebyContractProvider
from tokens.exceptions.exceptions import EmptyParamError
from tokens.models import Token
from RockNBlockTestTask.settings import CONFIG

logger = logging.getLogger('eventer')


def CreateToken(request) -> HttpResponse:
    logger.info('Handling request: method [tokens/create]')
    try:
        if request.method != 'POST':
            raise PermissionDenied
        request.headers.get('Content-Type', 'application/json')
        media_url = request.POST.get('media_url')
        owner = request.POST.get('owner')

        if media_url is None or media_url == '':
            raise EmptyParamError('media_url')
        if owner is None or owner == '':
            raise EmptyParamError('owner')
        logger.info("Got params from request: 'media url':'{}', 'owner':'{}'".format(media_url, owner))

        node = CONFIG['blockchain']['node_url']
        address = CONFIG['blockchain']['contract_address']
        abi = CONFIG['blockchain']['contract_abi']
        chain = CONFIG['blockchain']['chain_id']
        wallet_secret_key = CONFIG['blockchain']['wallet_secret']
        gas = CONFIG['blockchain']['gas']

        transaction = RinkebyContractProvider(
            BlockchainProvider(node_address=node), address, abi, chain
        ).mint(owner, media_url, gas, wallet_secret_key)
        transaction_details = json.loads(transaction)
        logger.info("Processing transaction: {}".format(transaction_details))
        token = Token.create(
            unique_hash=transaction_details['unique_hash'],
            tx_hash=transaction_details['tx_hash'],
            media_url=media_url,
            owner=owner
        )
        logger.info('Successfully request processed, response: {}'.format(token))
        status = 200
        msg = token.__str__()
    except EmptyParamError as error:
        status = 404
        msg = error.message
    except PermissionDenied:
        status = 403
        msg = "Required only 'POST' method"
    except web3.exceptions.ValidationError:
        status = 404
        msg = "Failed to 'mint' function process"
    finally:
        return JsonResponse(
            {'message': msg},
            status=status
        )


def ListTokens(request) -> HttpResponse:
    try:
        if request.method != 'GET':
            raise PermissionDenied
        logger.info('Handling request: method [tokens/list]')
        tokens = Token.objects.all()
        logger.info('Successfully request processed, response: {}'.format(tokens.__str__()))
        status = 200
        msg = tokens.__str__()
    except PermissionDenied:
        status = 403
        msg = "Required only 'GET' method"
    finally:
        return JsonResponse(
            {'message': msg},
            status=status
        )


def TokenTotalSupply(request) -> HttpResponse:
    try:
        if request.method != 'GET':
            raise PermissionDenied
        logger.info('Handling request: method [tokens/total_supply]')
        node = CONFIG['blockchain']['node_url']
        contract = CONFIG['blockchain']['contract_address']
        abi = CONFIG['blockchain']['contract_abi']
        chain = CONFIG['blockchain']['chain_id']

        supply = RinkebyContractProvider(
            blockchain_provider=BlockchainProvider(node_address=node),
            contract_abi=abi,
            contract_address=contract,
            chain_id=chain
        ).totalSupply()
        status = 200
        msg = 'Total supply: {}'.format(supply)
        logger.info('Successfully request processed, response: {}'.format(supply))
    except PermissionDenied:
        status = 403
        msg = "Required only 'GET' method"
    except web3.exceptions:
        status = 404
        msg = "Failed to 'totalSupply' function process"
    finally:
        return JsonResponse(
            {'message': msg},
            status=status
        )