from django import forms
from leads.models import Client
from agents.models import Agent

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['organization']

    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    # To override the agent field so organizations only can assign their agents to a client
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        organization = request.user.organization
        agents = Agent.objects.filter(organization=organization)
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['agent'].required = False
        self.fields['agent'].queryset = agents