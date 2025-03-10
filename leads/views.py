from django.shortcuts import reverse
from django.core.mail import send_mail
from leads.models import Client
from leads.forms import ClientForm
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class LeadDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'lead/lead_delete.html'

    def get_success_url(self):
        return reverse('leads:lead-list')

    def get_queryset(self):
        user = self.request.user

        # organizations only see their clients
        if user.is_organizor:
            queryset = Client.objects.filter(organization__user=user)

        # Agents only see their clients
        elif user.is_agent:
            queryset = Client.objects.filter(agent__user=user)

        return queryset

class LeadUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'lead/lead_update.html'
    form_class = ClientForm
    queryset = Client.objects.all()

    def get_success_url(self):
        return reverse('leads:lead-detail', args=[self.object.pk])

    def get_queryset(self):
        user = self.request.user

        # organizations only see their clients
        if user.is_organizor:
            queryset = Client.objects.filter(organization__user=user)

        # Agents only see their clients
        elif user.is_agent:
            queryset = Client.objects.filter(agent__user=user)

        return queryset

class LeadCreateView(LoginRequiredMixin, CreateView):
    template_name = 'lead/lead_form.html'
    form_class = ClientForm

    def get_success_url(self):
        return reverse('leads:lead-list')

    def form_valid(self, form):
        send_mail(
            subject='A lead has been created',
            message='visit the site to view the new lead',
            from_email='thenamelessone@tutamail.com',
            recipient_list=['x.kareem.x505@gmail.com']
        )
        return super(LeadCreateView, self).form_valid(form)

class LeadListView(LoginRequiredMixin, ListView):
    template_name = 'lead/lead_list.html'

    def get_queryset(self):
        user = self.request.user

        # organizations only see their clients
        if user.is_organizor:
            queryset = Client.objects.filter(organization__user=user)

        # Agents only see their clients
        elif user.is_agent:
            queryset = Client.objects.filter(agent__user=user)

        return queryset

class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = 'lead/lead_detail.html'

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