from django import forms
from accounts.models import User
from agents.models import Agent
from clients.models import Client

class AgentForm(forms.ModelForm):
    class Meta:
        model = User
        fields =  [
            'email',
            'username',
            'first_name',
            'last_name',
        ]

class AgentAssignForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['agent']

    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    # To override the agent field so organizations only can assign their agents to a client
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        organization = request.user.organization
        agents = Agent.objects.filter(organization=organization)
        super(AgentAssignForm, self).__init__(*args, **kwargs)
        self.fields['agent'].queryset = agents