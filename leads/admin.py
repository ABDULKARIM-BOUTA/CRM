from django.contrib import admin
from leads.models import Agent, Client, UserProfile

# Register your models here.
admin.site.register(Agent)
admin.site.register(Client)
admin.site.register(UserProfile)