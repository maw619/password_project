from django.test import TestCase
from django.urls import reverse

from .models import Credential


class CredentialViewsTests(TestCase):
    def test_create_credential(self):
        response = self.client.post(
            reverse("credential-create"),
            {
                "website_name": "Example",
                "website_url": "https://example.com",
                "username": "demo",
                "password": "supersecret",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Credential.objects.count(), 1)

    def test_list_credentials(self):
        Credential.objects.create(
            website_name="Example",
            website_url="https://example.com",
            username="demo",
            password="supersecret",
        )

        response = self.client.get(reverse("credential-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Example")
        self.assertContains(response, "https://example.com")
