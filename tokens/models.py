from django.db import models


class Token(models.Model):
    unique_hash = models.BigIntegerField()
    tx_hash = models.BigIntegerField()
    media_url = models.URLField()
    owner = models.TextField()
