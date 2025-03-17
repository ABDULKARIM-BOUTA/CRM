from django.urls import path
from accounts.views import PofilePageView, CustomPasswordChangeView

app_name = 'accounts'

urlpatterns = [
    path('', PofilePageView.as_view(), name='profile-page'),
]
