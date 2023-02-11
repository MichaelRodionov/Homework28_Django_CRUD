from django.urls import path

from ads.views import AdvertisementListView, AdvertisementDetailView, AdvertisementCreateView, AdvertisementUpdateView, \
    AdvertisementDeleteView, AdvertisementUploadImage

# ----------------------------------------------------------------
# advertisement urls
urlpatterns = [
    path('', AdvertisementListView.as_view()),
    path('create/', AdvertisementCreateView.as_view()),
    path('<int:pk>/', AdvertisementDetailView.as_view()),
    path('<int:pk>/update/', AdvertisementUpdateView.as_view()),
    path('<int:pk>/delete/', AdvertisementDeleteView.as_view()),
    path('<int:pk>/upload_image/', AdvertisementUploadImage.as_view())
]
