from random import choice
from string import ascii_uppercase, ascii_lowercase, digits

import web3.auto
import web3.eth
from web3 import Web3
from web3.middleware import geth_poa_middleware

from tokens.crypto.blockchain_base_provider import BlockChainBaseProvider


class BlockchainProvider(BlockChainBaseProvider):

    def __init__(self, node_address):
        self.node_address = node_address

    def mint(self, contract_address, contract_abi):
        pass

    def totalSupply(self, contract_address, contract_abi):
        contract = self.provider.eth.contract(address=contract_address, abi=contract_abi)
        res = contract.functions.totalSupply(74).call
        return res

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
        doc='Provider property'
    )
