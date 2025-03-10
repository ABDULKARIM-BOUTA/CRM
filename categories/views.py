from django.shortcuts import reverse
from categories.models import Category
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class CategoryListView(LoginRequiredMixin, ListView):
    template_name = 'category/category_list.html'
    queryset = Category.objects.all()

    def get_queryset(self):
        user = self.request.user

        # organizations only see their clients
        if user.is_organizor:
            queryset = Category.objects.filter(organization__user=user)

        # agents only see their clients
        elif user.is_agent:
            queryset = Category.objects.filter(agent_user=user)
            
        return queryset