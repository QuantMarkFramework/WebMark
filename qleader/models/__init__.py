from .result import Result  # noqa: F401
from .run import Run  # noqa: F401
from .run_scipy import RunScipy, RunScipyNelderMead, RunScipyBFGS  # noqa: F401
from .run_scipy import RunScipyLBFGSB, RunScipyCOBYLA  # noqa: F401
from .run_gradient import RunGradient   # noqa: F401
from .userprofile import UserProfile  # noqa: F401

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
