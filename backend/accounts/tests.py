from django.test import TestCase
from django.contrib.auth import get_user_model
from vendors.models import Vendor


User = get_user_model()


class AccountsSignalTest(TestCase):
    def test_vendor_auto_created_on_register(self):
        # create a user with role vendor
        user = User.objects.create_user(username='vendor_test', password='pass', role='vendor')
        # vendor profile should be auto-created by signal
        self.assertTrue(Vendor.objects.filter(user=user).exists())

    def test_customer_not_auto_vendor(self):
        user = User.objects.create_user(username='cust_test', password='pass', role='customer')
        self.assertFalse(Vendor.objects.filter(user=user).exists())
