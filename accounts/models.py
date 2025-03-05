from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

# Create your models here.

class User(AbstractUser):
    pass

    def __str__(self):
        return self.username

# this class helps to manage agents and clients under single portfolio
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


def post_create_user_signal(sender, created, instance, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(post_create_user_signal, sender=User)

