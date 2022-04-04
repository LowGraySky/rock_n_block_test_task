import logging
from random import choice
from string import ascii_uppercase, ascii_lowercase, digits

from web3.auto import w3
from web3 import Web3
from web3.middleware import geth_poa_middleware

from tokens.crypto.rinkeby_nft_contract_base_provider import RinkebyNFTContractBaseProvider


class RinkebyContractProvider(RinkebyNFTContractBaseProvider):

    def __init__(self, provider, contract_address, contract_abi):
        self.provider = provider
        self.contract_address = contract_address
        self.contract_abi = contract_abi

    def mint(self, owner, unique_hash, media_url, chain_id, recovery_hash):
        nonce = self.provider.eth.get_transaction_count(recovery_hash)
        mint = self.contract.functions\
            .mint(owner, unique_hash, media_url)\
            .buildTransaction({
                'chainId': chain_id,
                'gas': 70000,
                'maxFeePerGas': w3.toWei('2', 'gwei'),
                'maxPriorityFeePerGas': w3.toWei('1', 'gwei'),
                'nonce': nonce,
            })
        return mint

    def totalSupply(self):
        supply = self.contract.functions.totalSupply().call
        logging.info("get from total/supply function: total_supply:{}".format(supply))
        return supply

    def _get_contract(self):
        contract = self.provider.eth.contract(
            address=self.contract_address,
            abi=self.contract_abi)
        return contract

    contract = property(
        fget=_get_contract,
        doc='Contract property with http provider'
    )
