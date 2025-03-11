from django.urls import path
from categories.views import CategoryListView, CategoryDetailView, ClientCategoryUpdateView

app_name = 'categories'

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
    path('<int:pk>/detail/', CategoryDetailView.as_view(), name='category-detail'),
    path('<int:pk>/update/', ClientCategoryUpdateView.as_view(), name='category-update'),
]