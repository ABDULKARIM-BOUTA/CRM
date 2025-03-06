from django import forms
from agents.models import Agent

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = {
            'user'
        }