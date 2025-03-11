from django.shortcuts import reverse
from categories.models import Category
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Client
from categories.forms import CategoryUpdateForm

# Create your views here.

class CategoryListView(LoginRequiredMixin, ListView):
    template_name = 'category/category_list.html'

    def get_queryset(self):
        user = self.request.user

        if user.is_organizor:
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
        return queryset

    # to ge clients under specific category
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

class ClientCategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'category/category_update.html'
    form_class = CategoryUpdateForm
    queryset = Client.objects.all()

    def get_queryset(self):
        user = self.request.user

        if user.is_organizor:
            queryset = Client.objects.filter(organization__user=user)
        return queryset

    def get_success_url(self):
        return reverse('leads:lead-detail', args=[self.object.pk])

    def get_form_kwargs(self, **kwargs):
        kwargs = super(ClientCategoryUpdateView, self).get_form_kwargs(**kwargs)
        kwargs.update({'request': self.request})
        return kwargs