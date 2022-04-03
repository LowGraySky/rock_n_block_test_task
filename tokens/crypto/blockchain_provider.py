from random import choice
from string import ascii_uppercase, ascii_lowercase, digits

import web3.auto
import web3.eth

from tokens.crypto.blockchain_base_provider import BlockChainBaseProvider


class BlockchainProvider(BlockChainBaseProvider):

    def __init__(self, node_address):
        self.node_address = node_address

    def mint(self, contract_address, contract_abi):
       pass

    def totalSupply(self, contract_address, contract_abi):
        contract = web3.eth.Contract(address=contract_address)
        res = contract.functions.totalSupply().call
        return res

    @staticmethod
    def generateRandomRaw():
        values = digits + ascii_lowercase + ascii_uppercase
        random_number = ''.join(choice(values) for i in range(20))
        return random_number
