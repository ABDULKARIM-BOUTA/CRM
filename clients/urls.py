from django.urls import path
from clients.views import ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView

app_name = 'clients'

urlpatterns = [
    path('', ClientListView.as_view(), name='client-list'),
    path('<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('add/', ClientCreateView.as_view(), name='client-add'),
    path('<int:pk>/update/', ClientUpdateView.as_view(), name='client-update'),
    path('<int:pk>/delete/', ClientDeleteView.as_view(), name='client-delete'),

]