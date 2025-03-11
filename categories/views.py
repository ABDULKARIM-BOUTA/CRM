from django.shortcuts import reverse
from categories.models import Category
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Client

# Create your views here.

class CategoryListView(LoginRequiredMixin, ListView):
    template_name = 'category/category_list.html'
    queryset = Category.objects.all()


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