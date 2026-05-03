from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Credential(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="credentials", null=True, blank=True)
    website_name = models.CharField(max_length=255)
    website_url = models.URLField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["website_name"]

    def __str__(self) -> str:
        return f"{self.website_name} ({self.username})"
