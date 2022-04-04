from abc import ABCMeta, abstractmethod


class RinkebyNFTContractBaseProvider(metaclass=ABCMeta):

    @abstractmethod
    def mint(self, owner, unique_hash, media_url, chain_id, recovery_hash):
        raise NotImplementedError("Not implemented 'mint' method")

    @abstractmethod
    def totalSupply(self):
        raise NotImplementedError("Not implemented 'totalSupply' method")


    @abstractmethod
    def signTransaction(self, transaction, private_key):
        raise NotImplementedError("Not implemented 'signTransaction' method")

    @abstractmethod
    def sendTransaction(self, signed_transaction):
        raise NotImplementedError("Not implemented 'sendTransaction' method")
