from django.shortcuts import reverse
from categories.models import Category
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from clients.models import Client
from categories.forms import ClientCategoryUpdateForm, CategoryCreateForm
from agents.mixins import LoginAndOrganizorRequiredMixin

# Create your views here.

class CategoryListView(LoginRequiredMixin, ListView):
    template_name = 'category/category_list.html'

    def get_queryset(self):
        user = self.request.user

        # organizations only see their categories
        if user.is_organizor:
            queryset = Category.objects.filter(organization__user=user)

        # agents only see their categories
        if user.is_agent:
            queryset = Category.objects.filter(organization__user=user)

        return queryset

class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = 'category/category_detail.html'

    def get_queryset(self):
        user = self.request.user

        # organizations only see their clients
        if user.is_organizor:
            queryset = Category.objects.filter(organization__user=user)

        # agents only see their clients
        if user.is_agent:
            queryset = Category.objects.filter(organization__user=user)

        return queryset

    # to get clients under specific category
    # alternatively you can adjust category_detail.html to {% for client in category.clients.all %}
    # and it will function the same way
    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organizor:
            queryset = Client.objects.filter(organization__user=user)

        clients = self.get_object().clients.all()  # using the related name of the category FK. #get_object()can only be used in Detail
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
