from django.contrib import admin

from my_apps.models import Ads, Categories


admin.site.register(Categories)
admin.site.register(Ads)
