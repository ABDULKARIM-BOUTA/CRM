from django.shortcuts import reverse
from clients.models import Client
from clients.forms import ClientForm
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import LoginAndOrganizorRequiredMixin
# Create your views here.

class ClientDeleteView(LoginAndOrganizorRequiredMixin, DeleteView):
    template_name = 'client/client_delete.html'

    def get_success_url(self):
        return reverse('clients:client-list')

    def get_queryset(self):
        user = self.request.user

        # organizations only see their clients
        if user.is_organizor:
            queryset = Client.objects.filter(organization__user=user)

        return queryset

class ClientUpdateView(LoginAndOrganizorRequiredMixin, UpdateView):
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

        return queryset

class ClientCreateView(LoginAndOrganizorRequiredMixin, CreateView):
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

        return super(ClientCreateView, self).form_valid(form)

class ClientListView(LoginRequiredMixin, ListView):
    template_name = 'client/client_list.html'

    def get_queryset(self):
        user = self.request.user

        # Get the sort field and direction from the URL
        sort_field = self.request.GET.get('sort', 'sort_by_date')
        direction = self.request.GET.get('direction', 'asc')

        # Validate the sort field to prevent SQL injection
        valid_sort_fields = {'first_name', 'sort_by_date'}
        if sort_field not in valid_sort_fields:
            sort_field = 'first_name'

        # Add '-' prefix for descending order
        if direction == 'desc':
            sort_field = f'-{sort_field}'

        # Filter clients based on user role
        if user.is_organizor:
            queryset = Client.objects.filter(organization__user=user)
        elif user.is_agent:
            queryset = Client.objects.filter(agent__user=user)
        else:
            queryset = Client.objects.none()

        # Sort the queryset
        return queryset.order_by(sort_field)

    def get_context_data(self, **kwargs):
        # Add additional context data (sort_field and direction)
        context = super().get_context_data(**kwargs)
        context['sort_field'] = self.request.GET.get('sort', 'first_name')
        context['direction'] = self.request.GET.get('direction', 'asc')
        return context

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