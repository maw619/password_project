from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .models import Credential
# views.py
import csv
import io
import os
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

        fernet = Fernet(settings.PASSWORD_ENCRYPTION_KEY.encode())
        form.instance.password = fernet.encrypt(
            form.instance.password.encode()
        ).decode()

        return super().form_valid(form)


fernet = Fernet(settings.PASSWORD_ENCRYPTION_KEY.encode())

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

            encrypted_password = fernet.encrypt(password.encode()).decode()

            Credential.objects.create(
                owner=request.user,
                website_name=site,
                website_url=url,
                username=username,
                password=encrypted_password,
)

        return redirect("credential-list")

    return render(request, "uploads/import_passwords.html")