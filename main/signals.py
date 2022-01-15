from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models import signals

from . import services

User = get_user_model()


@receiver(signal=signals.post_save, sender=User)
def user_saved(**kwargs):
    user = kwargs.get('instance')
    if user.photo:
        services.watermark_photo(user.photo.path)
