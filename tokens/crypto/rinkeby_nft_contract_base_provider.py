from abc import ABCMeta, abstractmethod


class RinkebyNFTContractBaseProvider(metaclass=ABCMeta):

    @abstractmethod
    def mint(self, owner, unique_hash, media_url, chain_id, recovery_hash):
        raise NotImplementedError("Not implemented 'mint' method")

    @abstractmethod
    def totalSupply(self):
        raise NotImplementedError("Not implemented 'totalSupply' method")

