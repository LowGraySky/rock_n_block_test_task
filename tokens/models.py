import json

from django.db import models


class Token(models.Model):
    _id = models.BigAutoField(primary_key=True)
    _unique_hash = models.CharField(max_length=20, db_column='unique_hash')
    _tx_hash = models.CharField(max_length=100, blank=True, db_column='tx_hash')
    _media_url = models.URLField(db_column='media_url')
    _owner = models.CharField(max_length=42, db_column='owner')

    def _set_tx_hash(self, value):
        self._tx_hash = value

    def _get_tx_hash(self):
        return self._tx_hash

    def _get_id(self):
        return self._id

    def _get_unique_hash(self):
        return self._unique_hash

    def _get_media_url(self):
        return self._media_url

    def _get_owner(self):
        return self._owner

    @classmethod
    def create(cls, unique_hash, tx_hash, media_url, owner):
        token = cls(
            _unique_hash=unique_hash,
            _tx_hash=tx_hash,
            _media_url=media_url,
            _owner=owner
        )
        return token

    tx_hash = property(
        fget=_get_tx_hash,
        fset=_set_tx_hash
    )

    id = property(
        fget=_get_id
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

    def __unicode__(self):
        res = "Token:[unique_hash:{}, tx_hash:{}, media_url:{}, owner:{}]"\
            .format(self._unique_hash, self._tx_hash, self._media_url, self._owner)
        return res