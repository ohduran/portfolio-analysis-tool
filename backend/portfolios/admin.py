from django.contrib import admin
from .models import Portfolio, Investment


class PortfolioAdmin(admin.ModelAdmin):
    model = Portfolio
    list_display = [
        "name",
        "user",
    ]


admin.site.register(Portfolio, PortfolioAdmin)


class InvestmentAdmin(admin.ModelAdmin):
    model = Investment
    list_display = [
        "portfolio",
        "asset",
        "amount",
    ]


admin.site.register(Investment, InvestmentAdmin)
