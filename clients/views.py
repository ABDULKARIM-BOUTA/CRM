from django.shortcuts import reverse
from django.core.mail import send_mail
from clients.models import Client
from clients.forms import ClientForm
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class ClientDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'client/client_delete.html'

    def get_success_url(self):
        return reverse('clients:client-list')

    def get_queryset(self):
        user = self.request.user

        # organizations only see their clients
        if user.is_organizor:
            queryset = Client.objects.filter(organization__user=user)

        # Agents only see their clients
        elif user.is_agent:
            queryset = Client.objects.filter(agent__user=user)

        return queryset

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'client/client_update.html'
    form_class = ClientForm
    queryset = Client.objects.all()

    # it helps to override the agent field in the AgentAssignForm
    def get_form_kwargs(self, **kwargs):
        kwargs = super(ClientUpdateView, self).get_form_kwargs(**kwargs)
        kwargs.update({'request': self.request})
        return kwargs

    def get_success_url(self):
        return reverse('clients:client-detail', args=[self.object.pk])

    def get_queryset(self):
        user = self.request.user

        # organizations only see their clients
        if user.is_organizor:
            queryset = Client.objects.filter(organization__user=user)

        # Agents only see their clients
        elif user.is_agent:
            queryset = Client.objects.filter(agent__user=user)

        return queryset

class ClientCreateView(LoginRequiredMixin, CreateView):
    template_name = 'client/client_form.html'
    form_class = ClientForm

    # it helps to override the agent field in the AgentAssignForm
    def get_form_kwargs(self, **kwargs):
        kwargs = super(ClientCreateView, self).get_form_kwargs(**kwargs)
        kwargs.update({'request': self.request})
        return kwargs

    def get_success_url(self):
        return reverse('clients:client-list')

    def form_valid(self, form):

        # to set the client's organization as the user's organization by default
        form.instance.organization = self.request.user.organization

        send_mail(
            subject='A client has been created',
            message='visit the site to view the new lead',
            from_email='thenamelessone@tutamail.com',
            recipient_list=['x.kareem.x505@gmail.com']
        )
        return super(ClientCreateView, self).form_valid(form)

class ClientListView(LoginRequiredMixin, ListView):
    template_name = 'client/client_list.html'

    def get_queryset(self):
        user = self.request.user

        # organizations only see their clients
        if user.is_organizor:
            queryset = Client.objects.filter(organization__user=user)

        # Agents only see their clients
        elif user.is_agent:
            queryset = Client.objects.filter(agent__user=user)

        return queryset

class ClientDetailView(LoginRequiredMixin, DetailView):
    template_name = 'client/client_detail.html'

    def get_queryset(self):
        user = self.request.user

        # organizations only see their clients
        if user.is_organizor:
            queryset = Client.objects.filter(organization__user=user)

        # Agents only see their clients
        elif user.is_agent:
            queryset = Client.objects.filter(agent__user=user)

        return queryset

class LandingPageView(TemplateView):
    template_name = 'partials/landing_page.html'