from django.shortcuts import reverse
from django.views.generic import DetailView
from allauth.account.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User, Organization
from django.urls import reverse_lazy
from allauth.account.views import EmailView
from agents.mixins import LoginAndOrganizorRequiredMixin
from clients.models import Agent

# Create your views here.
class ProfilePageView(LoginRequiredMixin, DetailView):
    template_name = 'account/profile-page.html'
    model = User

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Add organization to context if the user is an agent
        if user.is_agent:
            try:
                agent = Agent.objects.get(user=user)
                context['organization'] = agent.organization
            except Agent.DoesNotExist:
                context['organization'] = None
        return context

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('accounts:profile-page')

class OrganizorEmailView(LoginAndOrganizorRequiredMixin, EmailView):
    """
    Custom email view that restricts access to authenticated organizors only.
    """
    pass