from django.db import models


class Token(models.Model):
    id = models.BigAutoField(primary_key=True)
    unique_hash = models.CharField(max_length=20, db_column='unique_hash')
    tx_hash = models.CharField(max_length=200, blank=True, db_column='tx_hash')
    media_url = models.URLField(db_column='media_url')
    owner = models.CharField(max_length=42, db_column='owner')

    @classmethod
    def create(cls, unique_hash, tx_hash, media_url, owner):
        token = cls(
            unique_hash=unique_hash,
            tx_hash=tx_hash,
            media_url=media_url,
            owner=owner
        )
        return token

    def __str__(self):
        return f"unique_hash: {self.unique_hash} tx_hash: {self.tx_hash} media_url: {self.media_url} owner: {self.owner}"
