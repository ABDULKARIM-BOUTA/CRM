from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail
from leads.models import Agent, Client
from leads.forms import ClientForm
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class LeadDeleteView(LoginRequiredMixin, DeleteView):
    queryset = Client.objects.all()
    template_name = 'lead/lead_delete.html'

    def get_success_url(self):
        return reverse('leads:lead-list')

class LeadUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'lead/lead_update.html'
    form_class = ClientForm
    queryset = Client.objects.all()

    def get_success_url(self):
        return reverse('leads:lead-detail', args=[self.object.pk])

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
        if self.request.user.is_organizor:
            queryset = Client.objects.all()

        if self.request.user.is_agent:
            queryset = Client.objects.filter(agent__user=self.request.user)

        return queryset

class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = 'lead/lead_detail.html'
    queryset = Client.objects.all()

class LandingPageView(TemplateView):
    template_name = 'partials/landing_page.html'