from abc import ABCMeta, abstractmethod


class RinkebyNFTContractBaseProvider(metaclass=ABCMeta):

    @abstractmethod
    def mint(self, owner, media_url, gas, wallet_secret, unique_hash):
        raise NotImplementedError("Not implemented 'mint' method")

    @abstractmethod
    def totalSupply(self):
        raise NotImplementedError("Not implemented 'totalSupply' method")

