from abc import ABCMeta, abstractmethod


class BlockchainBaseProvider(metaclass=ABCMeta):

    @abstractmethod
    def _get_provider(self):
        raise NotImplementedError("Not implemented '_get_provider' method")

    @abstractmethod
    def signTransaction(self, transaction, private_key):
        raise NotImplementedError("Not implemented 'signTransaction' method")

    @abstractmethod
    def sendTransaction(self, signed_transaction):
        raise NotImplementedError("Not implemented 'sendTransaction' method")

    @abstractmethod
    def signMessage(self, msg_for_sign, private_key):
        raise NotImplementedError("Not implemented 'signMessage' method")

    @abstractmethod
    def verifyMessage(self, msg_for_sign, signed_message):
        raise NotImplementedError("Not implemented 'verifyMessage' method")