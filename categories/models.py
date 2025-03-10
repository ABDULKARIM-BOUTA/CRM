from django.db import models
from accounts.models import Organization

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=30)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name