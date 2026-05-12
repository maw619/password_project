from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from .models import Credential
# views.py
import csv
import io
from cryptography.fernet import Fernet
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings


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

        form.instance.password = get_password_fernet().encrypt(
            form.instance.password.encode()
        ).decode()

        return super().form_valid(form)


class CredentialUpdateView(LoginRequiredMixin, UpdateView):
    model = Credential
    fields = ["website_name", "website_url", "username", "password"]
    template_name = "core/credential_form.html"
    success_url = reverse_lazy("credential-list")

    def get_queryset(self):
        return Credential.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        form.instance.password = get_password_fernet().encrypt(
            form.instance.password.encode()
        ).decode()

        return super().form_valid(form)


class CredentialDeleteView(LoginRequiredMixin, DeleteView):
    model = Credential
    success_url = reverse_lazy("credential-list")

    def get_queryset(self):
        return Credential.objects.filter(owner=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


@login_required
def bulk_delete_credentials(request):
    if request.method == "POST":
        credential_ids = request.POST.getlist("selected_credentials")
        if credential_ids:
            Credential.objects.filter(
                owner=request.user,
                id__in=credential_ids,
            ).delete()

    return redirect("credential-list")


def get_password_fernet():
    return Fernet(settings.PASSWORD_ENCRYPTION_KEY.encode())


@login_required
def import_chrome_passwords(request):
    if request.method == "POST":
        csv_file = request.FILES.get("password_csv")

        if not csv_file:
            return render(request, "import_passwords.html", {
                "error": "Please upload a CSV file."
            })

        decoded_file = csv_file.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(decoded_file))

        for row in reader:
            site = row.get("name", "")
            url = row.get("url", "")
            username = row.get("username", "")
            password = row.get("password", "")

            if not password:
                continue

            encrypted_password = get_password_fernet().encrypt(
                password.encode()
            ).decode()

            Credential.objects.create(
                owner=request.user,
                website_name=site,
                website_url=url,
                username=username,
                password=encrypted_password,
            )

        return redirect("credential-list")

    return render(request, "uploads/import_passwords.html")
