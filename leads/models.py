from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from accounts.models import User, UserProfile
from django.db.models.signals import post_save
from agents.models import Agent
# Create your models here.

# this class helps to manage agents and clients under single portfolio

class Client(models.Model): #this class stores the records of clients
    source_options = (
        ('1', 'Internet'),
        ('2', 'Newsletter'),
        ('3', 'TV'),
        ('4', 'Other')
    )

    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()

    source = models.CharField(max_length=50, choices=source_options)
    profile_picture = models.ImageField(blank=True, null=True)
    phoned = models.BooleanField(default=False)

    age = models.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(120)])
    files = models.FileField(blank=True, null=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


def post_create_user_signal(sender, created, instance, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(post_create_user_signal, sender=User)

