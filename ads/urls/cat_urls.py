from django.urls import path

from ads.views import CategoryListView, CategoryDetailView, CategoryUpdateView, CategoryDeleteView


# ----------------------------------------------------------------
# category urls
urlpatterns = [
    path('', CategoryListView.as_view()),
    path('<int:pk>/', CategoryDetailView.as_view()),
    path('<int:pk>/update/', CategoryUpdateView.as_view()),
    path('<int:pk>/delete/', CategoryDeleteView.as_view()),
]
