from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Homework28_Django_CRUD import settings
from ads.views import check_response
# from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', check_response),
    path('cat/', include('ads.urls.cat_urls')),
    path('ad/', include('ads.urls.ad_urls')),
    path('user/', include('users.urls.user_urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)