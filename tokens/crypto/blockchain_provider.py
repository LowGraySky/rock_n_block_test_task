from random import choice
from string import ascii_lowercase, digits, ascii_uppercase

from eth_account.messages import encode_defunct
from web3 import Web3
from web3.middleware import geth_poa_middleware

from tokens.crypto.blockchain_base_provide import BlockchainBaseProvider


class BlockchainProvider(BlockchainBaseProvider):

    def __init__(self, node_address):
        self.node_address = node_address

    def signTransaction(self, transaction, private_key):
        signed_transaction = self.provider.eth.account.sign_transaction(transaction, private_key=private_key)
        return signed_transaction

    def sendTransaction(self, signed_transaction):
        transfer = self.provider.eth.sendTransaction(signed_transaction.rawTransaction)
        return transfer

    def signMessage(self, msg_for_sign, private_key):
        message = encode_defunct(text=msg_for_sign)
        signed_message = self.provider.eth.account.sign_message(message, private_key=private_key)
        return signed_message

    def verifyMessage(self, msg_for_sign, signed_message):
        message = encode_defunct(text=msg_for_sign)
        recover_hash = self.provider.eth.account.recover_message(message, signature=signed_message.signature)
        return recover_hash

    @staticmethod
    def generateRandomRaw():
        values = digits + ascii_lowercase + ascii_uppercase
        random_number = ''.join(choice(values) for i in range(20))
        return random_number

    def _get_provider(self):
        provider = Web3(Web3.HTTPProvider(self.node_address))
        provider.middleware_onion.inject(geth_poa_middleware, layer=0)
        return provider

    provider = property(
        fget=_get_provider,
        doc='Http provider for current network node'
    )
