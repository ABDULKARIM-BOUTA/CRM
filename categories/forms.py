from django import forms
from clients.models import Client
from categories.models import Category

class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class ClientCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['category']

    category = forms.ModelChoiceField(queryset=Category.objects.none(), required=False)

    # To override the category field so organizations can only add their categories to their clients
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        organization = request.user.organization
        category = Category.objects.filter(organization=organization)
        super(ClientCategoryUpdateForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = category