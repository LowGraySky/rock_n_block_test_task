import logging
from random import choice
from string import ascii_lowercase, digits, ascii_uppercase

from eth_account.messages import encode_defunct
from web3 import Web3
from web3.middleware import geth_poa_middleware

from tokens.crypto.blockchain_base_provide import BlockchainBaseProvider

logger = logging.getLogger('crypter')


class BlockchainProvider(BlockchainBaseProvider):

    def __init__(self, node_address):
        super().__init__()
        self.node_address = node_address

    def signTransaction(self, transaction, private_key):
        signed_transaction = self.provider.eth.account.sign_transaction(transaction, private_key=private_key)
        logger.debug(
            "Sign transaction '{}' with private key '{}': {}".format(transaction, private_key, signed_transaction))
        return signed_transaction

    def sendRawTransaction(self, signed_transaction):
        transfer = self.provider.eth.send_raw_transaction(signed_transaction.rawTransaction)
        logger.debug("Send transaction '{}', got tx_hash: {}".format(signed_transaction, transfer))
        return transfer

    def signMessage(self, msg_for_sign, private_key):
        message = encode_defunct(text=msg_for_sign)
        signed_message = self.provider.eth.account.sign_message(message, private_key=private_key)
        logger.debug("Sign message '{}': {}".format(message, signed_message))
        return signed_message

    def verifyMessage(self, msg_for_sign, signed_message):
        message = encode_defunct(text=msg_for_sign)
        recover_hash = self.provider.eth.account.recover_message(message, signature=signed_message.signature)
        logger.debug("Got recovery hash for message '{}': {}".format(message, recover_hash))
        return recover_hash

    @staticmethod
    def generateRandomRaw() -> str:
        values = digits + ascii_lowercase + ascii_uppercase
        random_number = ''.join(choice(values) for i in range(20))
        logger.debug('Generate unique_hash(random number): {}'.format(random_number))
        return random_number

    def _get_provider(self):
        provider = Web3(Web3.HTTPProvider(self.node_address))
        provider.middleware_onion.inject(geth_poa_middleware, layer=0)
        logger.debug("Create HTTPProvider for node: {}".format(self.node_address))
        return provider

    provider = property(
        fget=_get_provider,
        doc='Http provider for current network node'
    )

    def _get_eth(self):
        eth = self.provider.eth
        return eth

    eth = property(
        fget=_get_eth,
    )
