from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .models import Credential


class CredentialListView(LoginRequiredMixin, ListView):
    model = Credential
    context_object_name = "credentials"
    template_name = "core/credential_list.html"

    def get_queryset(self):
        return Credential.objects.filter(owner=self.request.user)


class CredentialCreateView(LoginRequiredMixin, CreateView):
    model = Credential
    fields = ["website_name", "website_url", "username", "password"]
    template_name = "core/credential_form.html"
    success_url = reverse_lazy("credential-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
