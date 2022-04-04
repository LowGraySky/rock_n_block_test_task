import logging

from django.http import HttpResponse

from tokens.crypto.blockchain_provider import BlockchainProvider
from tokens.crypto.rinkeby_nft_contract_provider import RinkebyContractProvider
from tokens.models import Token
from RockNBlockTestTask.settings import CONFIG

logger = logging.getLogger('tokens_logger')


def CreateToken(reqeust, *args, **kwargs) -> HttpResponse:
    logger.info('Handling request: method [tokens/create] with params: [{}][{}]'.format(*args, **kwargs))

    url = reqeust.data.get('media_url')
    owner = reqeust.data.get('owner')
    node = CONFIG['blockchain']['node_url']
    contract = CONFIG['blockchain']['contract_address']
    abi = CONFIG['blockchain']['contract_abi']
    chain = CONFIG['blockchain']['chain_id']
    wallet_secret_key = CONFIG['blockchain']['wallet_secret']

    msg = 'Rock N Block message'
    blockchain_provider = BlockchainProvider(node_address=node)
    generated_hash = BlockchainProvider.generateRandomRaw()
    signed_msg = blockchain_provider.signMessage(
        msg_for_sign=msg,
        private_key=wallet_secret_key
    )
    rec_hash = blockchain_provider.verifyMessage(
        msg_for_sign=msg,
        signed_message=signed_msg
    )
    mint_transaction = RinkebyContractProvider(
        provider=blockchain_provider.provider,
        contract_abi=abi,
        contract_address=contract
    ).mint(
        owner=owner,
        unique_hash=generated_hash,
        media_url=url,
        chain_id=chain,
        recovery_hash=rec_hash
    )
    sign_transfer = blockchain_provider.signTransaction(
        transaction=mint_transaction,
        private_key=wallet_secret_key
    )
    tx_hash = blockchain_provider.sendTransaction(signed_transaction=sign_transfer)
    token = Token.create(
        unique_hash=generated_hash,
        tx_hash=tx_hash,
        media_url=url,
        owner=owner
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
    blockchain_provider = BlockchainProvider(node_address=node).provider
    supply = RinkebyContractProvider(
        provider=blockchain_provider,
        contract_abi=abi,
        contract_address=contract
    ).totalSupply()
    logger.info('Successfully request processed, response: {}'.format(supply))
    return HttpResponse('Total supply: {}'.format(supply))
