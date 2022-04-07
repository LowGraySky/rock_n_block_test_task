class TokenObject:

    def __init__(self, unique_hash, tx_hash, media_url, owner):
        self._unique_hash = unique_hash
        self._tx_hash = tx_hash
        self._media_url = media_url
        self._owner = owner

    def _set_tx_hash(self, value):
        self._tx_hash = value

    def _get_tx_hash(self):
        return self._tx_hash

    def _get_unique_hash(self):
        return self._unique_hash

    def _get_media_url(self):
        return self._media_url

    def _get_owner(self):
        return self._owner

    tx_hash = property(
        fget=_get_tx_hash,
        fset=_set_tx_hash
    )

    unique_hash = property(
        fget=_get_unique_hash
    )

    media_url = property(
        fget=_get_media_url
    )

    owner = property(
        fget=_get_owner
    )