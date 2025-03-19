from django.shortcuts import reverse
from django.views.generic import DetailView
from allauth.account.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User, Organization
from django.urls import reverse_lazy
from allauth.account.views import EmailView
from agents.mixins import LoginAndOrganizorRequiredMixin
from clients.models import Client

# Create your views here.
class PofilePageView(LoginRequiredMixin, DetailView):
    template_name = 'account/profile-page.html'
    model = User

    def get_object(self, queryset=None):
        return self.request.user

    def get_queryset(self):
        user = self.request.user

        # organizations only see their clients
        if user.is_organizor:
            queryset = Client.objects.filter(organization__user=user)

        # Agents only see their clients
        elif user.is_agent:
            queryset = Client.objects.filter(agent__user=user)

        return queryset

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('accounts:profile-page')

class OrganizorEmailView(LoginAndOrganizorRequiredMixin, EmailView):
    """
    Custom email view that restricts access to authenticated organizors only.
    """
    pass