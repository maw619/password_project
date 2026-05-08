from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings

User = get_user_model()


class Credential(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="credentials", null=True, blank=True)
    website_name = models.CharField(max_length=255)
    website_url = models.URLField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_decrypted_password(self):
        try:
            fernet = Fernet(settings.PASSWORD_ENCRYPTION_KEY.encode())
            return fernet.decrypt(self.password.encode()).decode()
        except InvalidToken:
            return self.password  # probably plain text / not encrypted yet
        except Exception:
            return "Unable to decrypt"
    class Meta:
        ordering = ["website_name"]

    def __str__(self) -> str:
        return f"{self.website_name} ({self.username})"
 

class PasswordEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    encrypted_password = models.TextField()
    url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)