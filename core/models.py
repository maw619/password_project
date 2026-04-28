from django.db import models


class Credential(models.Model):
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
