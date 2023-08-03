from django.contrib import admin
from .models import Asset, Alert, Rule


class AssetAdmin(admin.ModelAdmin):
    list_display = ['vehicle_type', 'vehicle_number']


admin.site.register(Asset, AssetAdmin)
admin.site.register(Alert)
admin.site.register(Rule)
