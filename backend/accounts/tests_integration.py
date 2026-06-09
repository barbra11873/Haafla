from django.test import TestCase
from rest_framework.test import APIClient


class JWTIntegrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/accounts/auth/register/'
        self.token_url = '/api/accounts/auth/token/'
        self.me_url = '/api/accounts/me/'
        self.vendors_url = '/api/vendors/vendors/'

    def test_register_obtain_token_and_get_me(self):
        payload = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'strongpassword',
            'role': 'customer',
        }
        # Register
        r = self.client.post(self.register_url, payload, format='json')
        self.assertIn(r.status_code, (200, 201))

        # Obtain token
        token_resp = self.client.post(self.token_url, {'username': 'testuser', 'password': 'strongpassword'}, format='json')
        self.assertEqual(token_resp.status_code, 200)
        access = token_resp.data.get('access')
        self.assertIsNotNone(access)

        # Use token to access /me/
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        me = self.client.get(self.me_url)
        self.assertEqual(me.status_code, 200)
        self.assertEqual(me.data.get('username'), 'testuser')

    def test_vendor_creation_requires_vendor_role(self):
        # Register as customer
        payload = {
            'username': 'cust1',
            'email': 'cust1@example.com',
            'password': 'pwcust1',
            'role': 'customer',
        }
        r = self.client.post(self.register_url, payload, format='json')
        self.assertIn(r.status_code, (200, 201))

        token_resp = self.client.post(self.token_url, {'username': 'cust1', 'password': 'pwcust1'}, format='json')
        access = token_resp.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

        # Attempt to create vendor profile should fail for non-vendor role
        create = self.client.post(self.vendors_url, {'display_name': 'X Co', 'bio': 'bio', 'location': 'here'}, format='json')
        self.assertIn(create.status_code, (400, 403))
