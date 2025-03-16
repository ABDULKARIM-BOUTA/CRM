from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class User(AbstractUser):
    # if you sign up you will automatically set as an organizor by default,
    # and if you add an agent that agent's account will be set as agent by default
    is_organizor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)

    def __str__(self):
        return self.username

# this class helps to manage agent and clients under single portfolio
class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

# Signal: when an account is created an Organization instance is automatically created
def post_create_user_signal(sender, created, instance, **kwargs):
    if created and instance.is_organizor:
        Organization.objects.create(user=instance)

post_save.connect(post_create_user_signal, sender=User)