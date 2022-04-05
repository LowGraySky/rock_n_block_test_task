import logging

from web3.auto import w3

from tokens.crypto.blockchain_provider import BlockchainProvider
from tokens.crypto.rinkeby_nft_contract_base_provider import RinkebyNFTContractBaseProvider

logger = logging.getLogger('crypter')


class RinkebyContractProvider(RinkebyNFTContractBaseProvider):

    def __init__(self, blockchain_provider, contract_address, contract_abi, chain_id):
        self.provider = blockchain_provider
        self.contract_address = contract_address
        self.contract_abi = contract_abi
        self.chain_id = chain_id

    def mint(self, owner: str,  media_url: str, gas: int, wallet_secret: str):
        msg = 'Rock N Block test message'
        owner_address = BlockchainProvider.addressFromString(address=owner)
        gen_hash = BlockchainProvider.generateRandomRaw()
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
            .mint(owner=owner_address,
                  unique_hash=gen_hash,
                  media_url=media_url) \
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
        tx_hash = self.provider.sendTransaction(signed_transaction=sign_transfer)
        return tx_hash

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
