from django.test import TestCase
from django.urls import reverse


class HomePageTests(TestCase):
    def test_home_page_returns_success(self):
        response = self.client.get(reverse("main:home"))

        self.assertEqual(response.status_code, 200)
