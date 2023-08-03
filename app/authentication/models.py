from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Datemodel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,  null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,  null=True, blank=True)


class Profile(Datemodel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100,  null=True, blank=True)
    user_photo = models.ImageField(
        upload_to='users_photo/',  null=True, blank=True)


@receiver(post_save, sender=User)
def create_profille(sender, instance, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=instance, email=instance.email)
