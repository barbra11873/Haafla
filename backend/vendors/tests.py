from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from vendors.models import Vendor

User = get_user_model()


class VendorApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor_user = User.objects.create_user(username='vuser', password='pass', role='vendor')
        self.customer_user = User.objects.create_user(username='cuser', password='pass', role='customer')

    def test_vendor_create_requires_vendor_role(self):
        # customer cannot create vendor profile
        self.client.login(username='cuser', password='pass')
        self.client.force_authenticate(user=self.customer_user)
        resp = self.client.post('/api/vendors/vendors/', {'display_name': 'Biz', 'bio': 'x'})
        self.assertEqual(resp.status_code, 403)

    def test_vendor_create_by_vendor(self):
        self.client.force_authenticate(user=self.vendor_user)
        resp = self.client.post('/api/vendors/vendors/', {'display_name': 'Biz', 'bio': 'x'})
        self.assertIn(resp.status_code, (200, 201))
        self.assertTrue(Vendor.objects.filter(user=self.vendor_user).exists())
