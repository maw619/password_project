from django.urls import path

from .views import (
    CredentialCreateView,
    CredentialDeleteView,
    CredentialListView,
    CredentialUpdateView,
    import_chrome_passwords,
)

urlpatterns = [
    path("", CredentialListView.as_view(), name="credential-list"),
    path("new/", CredentialCreateView.as_view(), name="credential-create"),
    path("<int:pk>/edit/", CredentialUpdateView.as_view(), name="credential-edit"),
    path("<int:pk>/delete/", CredentialDeleteView.as_view(), name="credential-delete"),
    path("import-passwords/", import_chrome_passwords, name="import_passwords"),
]
