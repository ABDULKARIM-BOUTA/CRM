from django.shortcuts import reverse
from categories.models import Category
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from clients.models import Client
from categories.forms import ClientCategoryUpdateForm, CategoryCreateForm
from agents.mixins import LoginAndOrganizorRequiredMixin
from agents.models import Agent
# Create your views here.

class CategoryListView(LoginRequiredMixin, ListView):
    template_name = 'category/category_list.html'

    def get_queryset(self):
        user = self.request.user

        # organizations only see their categories
        if user.is_organizor:
            queryset = Category.objects.filter(organization__user=user)

        # Agents see categories in their organization
        elif user.is_agent:
            try:
                # Get the agent's organization
                agent = Agent.objects.get(user=user)
                queryset = Category.objects.filter(organization=agent.organization)
            except Agent.DoesNotExist:
                queryset = Category.objects.none()  # No categories if agent has no organization

        else:
            queryset = Category.objects.none()  # Default to no categories for other users

        return queryset

class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = 'category/category_detail.html'

    def get_queryset(self):
        user = self.request.user

        if user.is_organizor:
            queryset = Category.objects.filter(organization__user=user)

        # Agents see categories in their organization
        elif user.is_agent:
            try:
                # Get the agent's organization
                agent = Agent.objects.get(user=user)
                queryset = Category.objects.filter(organization=agent.organization)
            except Agent.DoesNotExist:
                queryset = Category.objects.none()  # No categories if agent has no organization

        else:
            queryset = Category.objects.none()  # Default to no categories for other users

        return queryset

    # to get clients under specific category
    # alternatively you can adjust category_detail.html to {% for client in category.clients.all %}
    # and it will function the same way

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get the current category
        category = self.get_object()

        # Filter clients based on the user's role
        if user.is_organizor:
            # Organizers can see all clients under the category
            clients = category.clients.all()

        elif user.is_agent:
            try:
                # Agents can only see clients assigned to them under the category
                agent = Agent.objects.get(user=user)
                clients = category.clients.filter(agent=agent)
            except Agent.DoesNotExist:
                clients = category.clients.none()  # No clients if agent has no organization

        else:
            clients = category.clients.none()  # Default to no clients for other users

        # Add clients to the context
        context.update({'clients': clients})

        return context

class ClientCategoryUpdateView(LoginAndOrganizorRequiredMixin, UpdateView):
    template_name = 'category/client_category_update.html'
    form_class = ClientCategoryUpdateForm
    queryset = Client.objects.all()

    def get_queryset(self):
        user = self.request.user

        if user.is_organizor:
            queryset = Client.objects.filter(organization__user=user)
        return queryset

    def get_success_url(self):
        return reverse('clients:client-detail', args=[self.object.pk])

    def get_form_kwargs(self, **kwargs):
        kwargs = super(ClientCategoryUpdateView, self).get_form_kwargs(**kwargs)
        kwargs.update({'request': self.request})
        return kwargs

class CategoryCreateView(LoginAndOrganizorRequiredMixin, CreateView):
    template_name = 'category/category_create.html'
    form_class = CategoryCreateForm

    def get_success_url(self):
        return reverse('categories:category-list')

    def form_valid(self, form):
        form.instance.organization = self.request.user.organization
        return super(CategoryCreateView, self).form_valid(form)

class CategoryUpdateView(LoginAndOrganizorRequiredMixin, UpdateView):
    template_name = 'category/category_update.html'
    form_class = CategoryCreateForm

    def get_success_url(self):
        return reverse('categories:category-detail', args=[self.object.pk])

    def get_queryset(self):
        organization = self.request.user.organization
        return Category.objects.filter(organization=organization)

class CategoryDeleteView(LoginAndOrganizorRequiredMixin, DeleteView):
    template_name = 'category/category_delete.html'

    def get_success_url(self):
        return reverse('categories:category-list')

    def get_queryset(self):
        user = self.request.user

        # organizations only see their clients
        if user.is_organizor:
            queryset = Category.objects.filter(organization__user=user)
        return queryset
