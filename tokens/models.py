from django.db import models


class Token(models.Model):
    unique_hash = models.CharField(max_length=20, unique=True)
    tx_hash = models.CharField(max_length=200, blank=True)
    media_url = models.URLField()
    owner = models.CharField(max_length=42)
    send_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"id {self.id} unique_hash: {self.unique_hash} tx_hash: {self.tx_hash} media_url: {self.media_url} owner:{self.owner} send_at: {self.send_at}"
