from random import randint
from django.shortcuts import reverse
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from agents.forms import AgentForm
from agents.mixins import LoginAndOrganizorRequiredMixin
from agents.models import Agent
from django.core.mail import send_mail

# Create your views here.

class AgentListView(LoginAndOrganizorRequiredMixin, ListView):
    template_name = 'agent/agent_list.html'

    # to show agents related only to the user
    def get_queryset(self):
        organization = self.request.user.organization
        return Agent.objects.filter(organization=organization)

class AgentCreateView(LoginAndOrganizorRequiredMixin, CreateView):
    form_class = AgentForm
    template_name = 'agent/agent_form.html'

    def get_success_url(self):
        return reverse('agents:agent-list')

    # when an agent is add by the organization, an agent user is automatically created
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organizor = False

        # create a random password for the new agent
        user.set_password(f'{randint(0,1000000)}')
        user.save()

        Agent.objects.create(
            user=user,
            organization=self.request.user.organization
        )

        send_mail(
            subject='Email invitation',
            message=f'Please visit the website to confirm your account and set a new password' + '\n'                    
                    f'Username: {user.username}' + '\n' 
                    f'http://127.0.0.1:8000/accounts/password/reset/',
            from_email='thenamelessone@gmail.com',
            recipient_list=['kemo@gmail.com']
        )

        return super(AgentCreateView, self).form_valid(form)

class AgentDetailView(LoginAndOrganizorRequiredMixin, DetailView):
    template_name = 'agent/agent_detail.html'

    def get_queryset(self):
        organization = self.request.user.organization
        return Agent.objects.filter(organization=organization)

class AgentDeleteView(LoginAndOrganizorRequiredMixin, DeleteView):
    template_name = 'agent/agent_delete.html'

    def get_success_url(self):
        return reverse('agents:agent-list')

    def get_queryset(self):
        organization = self.request.user.organization
        return Agent.objects.filter(organization=organization)

class AgentUpdateView(LoginAndOrganizorRequiredMixin, UpdateView):
    form_class = AgentForm
    template_name = 'agent/agent_update.html'

    def get_success_url(self):
        return reverse('agents:agent-detail', args=[self.object.pk])

    def get_queryset(self):
        organization = self.request.user.organization
        return Agent.objects.filter(organization=organization)
