from django.urls import path
from categories.views import CategoryListView, CategoryDetailView, ClientCategoryUpdateView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView

app_name = 'categories'

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
    path('create/', CategoryCreateView.as_view(), name='category-create'),
    path('<int:pk>/detail/', CategoryDetailView.as_view(), name='category-detail'),
    path('<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    path('<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('<int:pk>/client-update/', ClientCategoryUpdateView.as_view(), name='client-category-update'),
]