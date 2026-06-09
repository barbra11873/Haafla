from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.apps import apps


User = get_user_model()


@receiver(post_save, sender=User)
def create_vendor_on_register(sender, instance, created, **kwargs):
    if not created:
        return
    try:
        if getattr(instance, 'role', None) == 'vendor':
            Vendor = apps.get_model('vendors', 'Vendor')
            # create vendor profile if not exists
            if not Vendor.objects.filter(user=instance).exists():
                Vendor.objects.create(user=instance, display_name=instance.username)
    except Exception:
        # fail silently; logging can be added
        pass
