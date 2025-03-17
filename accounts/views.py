from django.shortcuts import reverse
from django.views.generic import DetailView
from allauth.account.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User
from django.urls import reverse_lazy

# Create your views here.
class PofilePageView(LoginRequiredMixin, DetailView):
    template_name = 'account/profile-page.html'
    model = User

    def get_object(self, queryset=None):
        return self.request.user

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('accounts:profile-page')
