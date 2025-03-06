from django.shortcuts import reverse
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from agents.forms import AgentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.models import Agent

# Create your views here.

class AgentListView(LoginRequiredMixin, ListView):
    template_name = 'agent/agent_list.html'

    # to show agents related only to the user
    def get_queryset(self):
        organization = self.request.user.organization
        return Agent.objects.filter(organization=organization)

class AgentCreateView(LoginRequiredMixin, CreateView):
    form_class = AgentForm
    template_name = 'agent/agent_form.html'

    def get_success_url(self):
        return reverse('agents:agent-list')

    # to add the agent to the current user without doing it manually
    def form_valid(self, form):
        agent = form.save(commit=False)
        agent.organization = self.request.user.organization
        agent.save()
        return super(AgentCreateView, self).form_valid(form)

class AgentDetailView(LoginRequiredMixin, DetailView):
    template_name = 'agent/agent_detail.html'

    def get_queryset(self):
        organization = self.request.user.organization
        return Agent.objects.filter(organization=organization)


class AgentDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'agent/agent_delete.html'

    def get_success_url(self):
        return reverse('agents:agent-list')

    def get_queryset(self):
        organization = self.request.user.organization
        return Agent.objects.filter(organization=organization)

class AgentUpdateView(LoginRequiredMixin, UpdateView):
    form_class = AgentForm
    template_name = 'agent/agent_update.html'

    def get_success_url(self):
        return reverse('agents:agent-detail', args=[self.object.pk])

    def get_queryset(self):
        organization = self.request.user.organization
        return Agent.objects.filter(organization=organization)
