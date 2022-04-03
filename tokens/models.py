import json

from django.db import models


class Token(models.Model):
    id = models.BigAutoField(primary_key=True)
    unique_hash = models.CharField(max_length=20)
    tx_hash = models.BigIntegerField()
    media_url = models.URLField()
    owner = models.CharField(max_length=42)