from django.db import models
from accounts.models import User, Organization
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.
class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


# Signal to delete the associated User when an Agent is deleted
@receiver(post_delete, sender=Agent)
def delete_associated_user(sender, instance, **kwargs):
    if instance.user: 
        instance.user.delete()