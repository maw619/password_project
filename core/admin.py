from django.contrib import admin

from .models import Credential


@admin.register(Credential)
class CredentialAdmin(admin.ModelAdmin):
    list_display = ("website_name", "website_url", "username", "updated_at")
    search_fields = ("website_name", "website_url", "username")
