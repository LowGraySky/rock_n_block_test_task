from abc import ABCMeta, abstractmethod


class BlockChainBaseProvider(metaclass=ABCMeta):

    @abstractmethod
    def mint(self, contract_address, contract_abi):
        raise NotImplementedError("Not implemented 'mint' method")

    @abstractmethod
    def totalSupply(self, contract_address, contract_abi):
        raise NotImplementedError("Not implemented 'totalSupply' method")
