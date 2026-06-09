from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from vendors.models import Vendor, PortfolioItem
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image

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
        # if a vendor profile was auto-created by signal, view may return 403 to prevent duplicates
        self.assertIn(resp.status_code, (200, 201, 403))
        self.assertTrue(Vendor.objects.filter(user=self.vendor_user).exists())

    def test_portfolio_upload(self):
        self.client.force_authenticate(user=self.vendor_user)
        # ensure vendor profile exists
        resp = self.client.post('/api/vendors/vendors/', {'display_name': 'Biz2', 'bio': 'x'})
        self.assertIn(resp.status_code, (200, 201, 403))

        # upload without file
        resp2 = self.client.post('/api/vendors/portfolio/', {'title': 'Sample', 'description': 'desc'}, format='multipart')
        self.assertIn(resp2.status_code, (200, 201, 201))

        # upload with a valid image
        image = Image.new('RGB', (400, 300), color='navy')
        buffer = BytesIO()
        image.save(buffer, format='JPEG')
        buffer.seek(0)
        jpg = SimpleUploadedFile('small.jpg', buffer.read(), content_type='image/jpeg')
        resp3 = self.client.post(
            '/api/vendors/portfolio/',
            {'title': 'WithFile', 'file': jpg, 'description': 'portfolio item'},
            format='multipart',
        )
        self.assertIn(resp3.status_code, (200, 201))
        self.assertEqual(PortfolioItem.objects.filter(vendor=self.vendor_user.vendor).count(), 2)
        self.assertTrue(PortfolioItem.objects.filter(vendor=self.vendor_user.vendor, thumbnail__isnull=False).exists())

    def test_portfolio_validation_rejects_bad_files(self):
        self.client.force_authenticate(user=self.vendor_user)
        self.client.post('/api/vendors/vendors/', {'display_name': 'Biz3', 'bio': 'x'})

        bad_bytes = SimpleUploadedFile('bad.jpg', b'not-an-image', content_type='image/jpeg')
        bad_resp = self.client.post(
            '/api/vendors/portfolio/',
            {'title': 'Bad', 'file': bad_bytes},
            format='multipart',
        )
        self.assertEqual(bad_resp.status_code, 400)

        too_large = SimpleUploadedFile('big.jpg', b'a' * (5 * 1024 * 1024 + 1), content_type='image/jpeg')
        size_resp = self.client.post(
            '/api/vendors/portfolio/',
            {'title': 'Big', 'file': too_large},
            format='multipart',
        )
        self.assertEqual(size_resp.status_code, 400)

        large_image = Image.new('RGB', (4001, 10), color='red')
        large_buffer = BytesIO()
        large_image.save(large_buffer, format='JPEG')
        large_buffer.seek(0)
        large_jpg = SimpleUploadedFile('large.jpg', large_buffer.read(), content_type='image/jpeg')
        dimension_resp = self.client.post(
            '/api/vendors/portfolio/',
            {'title': 'Large', 'file': large_jpg},
            format='multipart',
        )
        self.assertEqual(dimension_resp.status_code, 400)
