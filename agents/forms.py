from django import forms
from accounts.models import User

class AgentForm(forms.ModelForm):
    class Meta:
        model = User
        fields =  [
            'email',
            'username',
            'first_name',
            'last_name',

        ]