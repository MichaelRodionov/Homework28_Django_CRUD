from django.contrib import admin

from ads.models import Advertisement, Category
from users.models import User, Location


# ----------------------------------------------------------------
# admin register models
admin.site.register(Advertisement)
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(User)
