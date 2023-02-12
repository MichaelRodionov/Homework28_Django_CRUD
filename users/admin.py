from django.contrib import admin

from users.models import Location, User


# ----------------------------------------------------------------
# admin register models
admin.site.register(Location)
admin.site.register(User)
