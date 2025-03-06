from django.urls import path
from agents.views import AgentCreateView, AgentListView, AgentDetailView, AgentDeleteView, AgentUpdateView

app_name = 'agents'

urlpatterns = [
    path('', AgentListView.as_view(), name='agent-list'),
    path('add/', AgentCreateView.as_view(), name='agent-form'),
    path('<int:pk>/', AgentDetailView.as_view(), name='agent-detail'),
    path('<int:pk>/delete/', AgentDeleteView.as_view(), name='agent-delete'),
    path('<int:pk>/update/', AgentUpdateView.as_view(), name='agent-update'),
]