from django.db import models
from django.conf import settings


class EventPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    input_json = models.JSONField()
    output_json = models.JSONField(null=True, blank=True)
    provider = models.CharField(max_length=100, default='openai')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"EventPlan {self.id} by {self.user.username}"
