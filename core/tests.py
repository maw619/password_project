from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from .models import Credential
from .views import CredentialListView


TEST_ENCRYPTION_KEY = "cp9Id8P3FjKkEhLdd_HdlFZotABbBSLkxJ4l7qGrD2s="


@override_settings(PASSWORD_ENCRYPTION_KEY=TEST_ENCRYPTION_KEY)
class CredentialViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="demo-user",
            password="test-password",
        )
        self.other_user = get_user_model().objects.create_user(
            username="other-user",
            password="test-password",
        )
        self.client.force_login(self.user)
        self.factory = RequestFactory()

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
        credential = Credential.objects.get()
        self.assertEqual(credential.owner, self.user)
        self.assertEqual(credential.get_decrypted_password(), "supersecret")

    def test_list_credentials(self):
        Credential.objects.create(
            owner=self.user,
            website_name="Example",
            website_url="https://example.com",
            username="demo",
            password="supersecret",
        )
        Credential.objects.create(
            owner=self.other_user,
            website_name="Other Example",
            website_url="https://other.example.com",
            username="other",
            password="supersecret",
        )

        request = self.factory.get(reverse("credential-list"))
        request.user = self.user

        response = CredentialListView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context_data["credentials"]),
            [Credential.objects.get(owner=self.user)],
        )

    def test_bulk_delete_credentials_deletes_selected_owned_credentials_only(self):
        first = Credential.objects.create(
            owner=self.user,
            website_name="First",
            website_url="https://first.example.com",
            username="first",
            password="supersecret",
        )
        second = Credential.objects.create(
            owner=self.user,
            website_name="Second",
            website_url="https://second.example.com",
            username="second",
            password="supersecret",
        )
        unselected = Credential.objects.create(
            owner=self.user,
            website_name="Unselected",
            website_url="https://unselected.example.com",
            username="unselected",
            password="supersecret",
        )
        other_user_credential = Credential.objects.create(
            owner=self.other_user,
            website_name="Other User",
            website_url="https://other-user.example.com",
            username="other",
            password="supersecret",
        )

        response = self.client.post(
            reverse("credential-bulk-delete"),
            {
                "selected_credentials": [
                    first.id,
                    second.id,
                    other_user_credential.id,
                ],
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("credential-list"))
        self.assertFalse(
            Credential.objects.filter(id__in=[first.id, second.id]).exists()
        )
        self.assertTrue(Credential.objects.filter(id=unselected.id).exists())
        self.assertTrue(
            Credential.objects.filter(id=other_user_credential.id).exists()
        )

    def test_bulk_delete_without_selection_keeps_credentials(self):
        credential = Credential.objects.create(
            owner=self.user,
            website_name="Keep Me",
            website_url="https://keep.example.com",
            username="keeper",
            password="supersecret",
        )

        response = self.client.post(reverse("credential-bulk-delete"), {})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("credential-list"))
        self.assertTrue(Credential.objects.filter(id=credential.id).exists())
