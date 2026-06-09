from django.db import models


class OnChainTx(models.Model):
    related_type = models.CharField(max_length=100)
    related_id = models.IntegerField()
    tx_hash = models.CharField(max_length=200)
    network = models.CharField(max_length=100, default='testnet')
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.related_type}:{self.related_id} - {self.tx_hash} ({self.status})"
