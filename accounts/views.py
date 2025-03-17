from django.shortcuts import reverse
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User

# Create your views here.
class PofilePageView(LoginRequiredMixin, DetailView):
    template_name = 'account/profile-page.html'
    model = User

    def get_object(self, queryset=None):
        return self.request.user