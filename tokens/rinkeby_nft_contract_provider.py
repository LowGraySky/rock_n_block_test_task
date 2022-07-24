import json
import logging

from django.conf import settings
from web3 import Web3
from web3.auto import w3

from tokens.blockchain_provider import BlockchainProvider

logger = logging.getLogger("crypter")


class RinkebyContractProvider:
    def __init__(self, provider: BlockchainProvider):
        self.provider = provider

    def mint(self, owner: str, media_url: str, unique_hash: str):
        msg = "Rock N Block test message"
        if not Web3.isAddress(owner):
            raise ValueError("Incorrect address provided: '{}'".format(owner))
        signed_msg = self.provider.signMessage(msg_for_sign=msg)
        recovery_hash = self.provider.verifyMessage(
            msg_for_sign=msg, signed_message=signed_msg
        )
        nonce = self.provider.eth.get_transaction_count(recovery_hash)
        mint = self.contract.functions.mint(
            owner, unique_hash, media_url
        ).buildTransaction(
            {
                "chainId": settings.CHAIN_ID,
                "gas": settings.GAS,
                "maxFeePerGas": w3.toWei("2", "gwei"),
                "maxPriorityFeePerGas": w3.toWei("1", "gwei"),
                "nonce": nonce,
            }
        )
        sign_transfer = self.provider.signTransaction(transaction=mint)
        tx_hash = self.provider.sendRawTransaction(signed_transaction=sign_transfer)
        transaction_obj = json.dumps(
            {
                "unique_hash": unique_hash,
                "tx_hash": str(tx_hash),
                "gas": settings.GAS,
                "recovery_hash": recovery_hash,
                "nonce": nonce,
            }
        )
        return transaction_obj

    def totalSupply(self):
        supply = self.contract.functions.totalSupply().call()
        logger.debug("Total_supply:{}".format(supply))
        return supply

    @staticmethod
    def get_abi():
        abi = None
        with open(settings.ABI) as f:
            abi += "".join(f.readlines())
        return abi

    def _get_contract(self):
        contract_address = Web3.toChecksumAddress(settings.CONTRACT_ADDRESS)
        logger.debug("To check sum address: {}".format(contract_address))
        contract = self.provider.eth.contract(
            address=contract_address, abi=RinkebyContractProvider.get_abi()
        )
        logger.debug("Contract object created: {}".format(contract.address))
        return contract

    contract = property(fget=_get_contract, doc="Contract property with http provider")
