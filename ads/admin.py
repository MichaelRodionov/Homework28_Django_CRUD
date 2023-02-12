from django.contrib import admin

from ads.models import Advertisement, Category


# ----------------------------------------------------------------
# admin register models
admin.site.register(Advertisement)
admin.site.register(Category)

