from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    national_id = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.first_name

    @receiver(post_save, sender=User)
    def create_user_profile(self, sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(self, sender, instance, **kwargs):
        instance.profile.save()