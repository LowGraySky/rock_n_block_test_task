import json
import logging

from eth_utils import to_text
from web3 import Web3
from web3.auto import w3

from tokens.crypto.blockchain_provider import BlockchainProvider
from tokens.crypto.rinkeby_nft_contract_base_provider import RinkebyNFTContractBaseProvider

logger = logging.getLogger('crypter')


class RinkebyContractProvider(RinkebyNFTContractBaseProvider):

    def __init__(self, blockchain_provider: BlockchainProvider, contract_address, contract_abi, chain_id):
        self.provider = blockchain_provider
        self.contract_address = contract_address
        self.contract_abi = contract_abi
        self.chain_id = chain_id

    def mint(self, owner: str,  media_url: str, gas: int, wallet_secret: str, unique_hash: str):
        msg = 'Rock N Block test message'
        if not Web3.isAddress(owner):
            raise ValueError("Incorrect address provided: '{}'".format(owner))
        signed_msg = self.provider.signMessage(
            msg_for_sign=msg,
            private_key=wallet_secret
        )
        recovery_hash = self.provider.verifyMessage(
            msg_for_sign=msg,
            signed_message=signed_msg
        )
        nonce = self.provider.eth.get_transaction_count(recovery_hash)
        mint = self.contract.functions \
            .mint(owner,
                  unique_hash,
                  media_url) \
            .buildTransaction({
                'chainId': self.chain_id,
                'gas': gas,
                'maxFeePerGas': w3.toWei('2', 'gwei'),
                'maxPriorityFeePerGas': w3.toWei('1', 'gwei'),
                'nonce': nonce,
            }
        )
        sign_transfer = self.provider.signTransaction(
            transaction=mint,
            private_key=wallet_secret
        )
        tx_hash = self.provider.sendRawTransaction(signed_transaction=sign_transfer)
        transaction_obj = json.dumps(
            {
                'unique_hash': unique_hash,
                'tx_hash': str(tx_hash),
                'gas': gas,
                'recovery_hash': recovery_hash,
                'nonce': nonce
            }
        )
        return transaction_obj

    def totalSupply(self):
        supply = self.contract.functions.totalSupply().call()
        logger.debug("Total_supply:{}".format(supply))
        return supply

    def _get_contract(self):
        contract_address = Web3.toChecksumAddress(self.contract_address)
        logger.debug("To check sum address: {}".format(contract_address))
        contract = self.provider.eth.contract(
            address=contract_address,
            abi=self.contract_abi)
        logger.debug("Contract object created: {}".format(contract.address))
        return contract

    contract = property(
        fget=_get_contract,
        doc='Contract property with http provider'
    )
