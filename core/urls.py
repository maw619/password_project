from django.urls import path

from .views import CredentialCreateView, CredentialListView, import_chrome_passwords

urlpatterns = [
    path("", CredentialListView.as_view(), name="credential-list"),
    path("new/", CredentialCreateView.as_view(), name="credential-create"),
    path("import-passwords/", import_chrome_passwords, name="import_passwords"),
]
