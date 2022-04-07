import json
import logging

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
        status = 'result'
        status_code = 200
        msg = "Token: {}".format(token.__str__())
    except EmptyParamError as error:
        status = 'error'
        status_code = 400
        msg = error.message
    except PermissionDenied:
        status = 'error'
        status_code = 403
        msg = "Required only 'POST' method"
    except Exception as error:
        status = 'error'
        status_code = 400
        msg = "Failed to process 'mint' function: {}".format(error)
    finally:
        return JsonResponse(
            {'status': status, 'message': msg},
            status=status_code
        )


def ListTokens(request) -> HttpResponse:
    try:
        if request.method != 'GET':
            raise PermissionDenied
        logger.info('Handling request: method [tokens/list]')
        tokens = Token.objects.all()
        logger.info('Successfully request processed, response: {}'.format(tokens.__str__()))
        status = 'result'
        status_code = 200
        msg = tokens.__str__()
    except PermissionDenied:
        status = 'error'
        status_code = 403
        msg = "Required only 'GET' method"
    except Exception as error:
        status = 'error'
        status_code = 400
        msg = "Failed to process 'list' function: {}".format(error)
    finally:
        return JsonResponse(
            {'status': status, 'message': msg},
            status=status_code
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
        status = 'result'
        status_code = 200
        msg = 'Total supply: {}'.format(supply)
        logger.info('Successfully request processed, response: {}'.format(supply))
    except PermissionDenied:
        status = 'error'
        status = 403
        msg = "Required only 'GET' method"
    except Exception as error:
        status = 'error'
        status_code = 400
        msg = "Failed to process 'totolSupply' function: {}".format(error)
    finally:
        return JsonResponse(
            {'status': status, 'message': msg},
            status=status_code
        )
