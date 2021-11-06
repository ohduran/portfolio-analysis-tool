from django.contrib import admin
from .models import Asset, HistoricValue


class AssetAdmin(admin.ModelAdmin):
    model = Asset
    list_display = ["name", "symbol", "sector"]


admin.site.register(Asset, AssetAdmin)


class HistoricValueAdmin(admin.ModelAdmin):
    model = HistoricValue
    list_display = ["asset", "date_time", "close"]


admin.site.register(HistoricValue, HistoricValueAdmin)
