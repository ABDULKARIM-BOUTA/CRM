from django.urls import path
from accounts.views import ProfilePageView

app_name = 'accounts'

urlpatterns = [
    path('', ProfilePageView.as_view(), name='profile-page'),
]
