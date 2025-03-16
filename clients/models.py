from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from agents.models import Agent
from accounts.models import Organization
from categories.models import Category

# Create your models here.

class Client(models.Model): #this class stores the records of clients
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    age = models.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(120)])
    phone_number = models.CharField(max_length=20)
    date_added = models.DateField(auto_now_add=True)
    sort_by_date = models.DateTimeField(auto_now_add=True)

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE) # If an organization got deleted all clients under that organization will be deleted
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True) # If an agent got deleted all clients under that agent will be set to null
    category = models.ForeignKey(Category, related_name='clients', on_delete=models.SET_NULL, null=True, blank=True) # If a category got deleted all clients under that category will be set to null

    def __str__(self):
        return f'{self.first_name} {self.last_name}'