from django import forms
from accounts.models import User
from agents.models import Agent
from clients.models import Client
from django.core.exceptions import ValidationError

class AgentUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField(max_length=15)
    first_name = forms.CharField(max_length=20, required=False)
    last_name = forms.CharField(max_length=20, required=False)

    class Meta:
        model = Agent
        exclude = ['user','organization']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email
            self.fields['username'].initial = self.instance.user.username
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError("Email is required.")

        # Check if the email is already in use by another user
        user_with_email = User.objects.filter(email=email).exclude(pk=self.instance.user.pk).first()
        if user_with_email:
            raise ValidationError("This email is already in use by another user.")

        return email

    def save(self, commit=True):
        agent = super().save(commit=False)
        if commit:
            agent.save()
            user = agent.user
            user.email = self.cleaned_data['email']
            user.username = self.cleaned_data['username']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.save()
        return agent


class AgentCreateForm(forms.ModelForm):
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