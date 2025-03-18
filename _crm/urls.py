from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from clients.views import LandingPageView
from django.contrib.auth.views import LoginView, LogoutView
from allauth.account.views import EmailView
from accounts.views import CustomPasswordChangeView, OrganizorEmailView
#from accounts.views import SignUpView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing-page'),
    path('clients/', include('clients.urls', namespace='clients')),
    path('agents/', include('agents.urls', namespace='agents')),
    path('categories/', include('categories.urls', namespace='categories')),
    path('profile/', include('accounts.urls', namespace='profile')),
    path('accounts/password/change/', CustomPasswordChangeView.as_view(), name='change-password'),
    path('accounts/email/', OrganizorEmailView.as_view(), name='account_email'),
    path('accounts/', include('allauth.urls')),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)