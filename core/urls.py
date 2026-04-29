from django.urls import path

from .views import CredentialCreateView, CredentialListView

urlpatterns = [
    path("", CredentialListView.as_view(), name="credential-list"),
    path("new/", CredentialCreateView.as_view(), name="credential-create"),
]
