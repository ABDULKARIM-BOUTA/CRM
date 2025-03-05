from django.db import models
from accounts.models import User, UserProfile

# Create your models here.


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
