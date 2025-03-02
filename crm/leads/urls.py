from django.urls import path
from leads.views import lead_list, lead_detail, lead_add, lead_update, lead_delete

app_name = 'leads'

urlpatterns = [
    path('', lead_list, name='lead-list'),
    path('<int:pk>/', lead_detail, name='lead-detail'),
    path('add/', lead_add, name='lead-add'),
    path('<int:pk>/update/', lead_update, name='lead-update'),
    path('<int:pk>/delete/', lead_delete, name='lead-delete'),

]