from django.db import models
from django.db.models.fields import CharField,  TextField
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    real_name = CharField(max_length=30, blank=True)
    institution = CharField(max_length=30, blank=True)
    bio = TextField(max_length=500, blank=True)

    def __str__(self):
        return f'UserProfile: {self.user}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
