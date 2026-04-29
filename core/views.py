from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .models import Credential


class CredentialListView(ListView):
    model = Credential
    context_object_name = "credentials"
    template_name = "core/credential_list.html"


class CredentialCreateView(CreateView):
    model = Credential
    fields = ["website_name", "website_url", "username", "password"]
    template_name = "core/credential_form.html"
    success_url = reverse_lazy("credential-list")
