from django.urls import path

from .views import (
    CredentialCreateView,
    CredentialDeleteView,
    CredentialListView,
    CredentialUpdateView,
    bulk_delete_credentials,
    import_chrome_passwords,
)

urlpatterns = [
    path("", CredentialListView.as_view(), name="credential-list"),
    path("new/", CredentialCreateView.as_view(), name="credential-create"),
    path("bulk-delete/", bulk_delete_credentials, name="credential-bulk-delete"),
    path("<int:pk>/edit/", CredentialUpdateView.as_view(), name="credential-edit"),
    path("<int:pk>/delete/", CredentialDeleteView.as_view(), name="credential-delete"),
    path("import-passwords/", import_chrome_passwords, name="import_passwords"),
]
