from django.urls import path
from categories.views import CategoryListView, CategoryDetailView

app_name = 'categories'

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
    path('<int:pk>/detail/', CategoryDetailView.as_view(), name='category-detail'),
]