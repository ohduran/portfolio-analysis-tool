from assets.models import Asset, HistoricValue
from django.db.models import Prefetch
from portfolios import serializers
from portfolios.models import Portfolio
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = (
        Portfolio.objects.active()
        .prefetch_related("investments")
        .prefetch_related("investments__asset__historic_values")
        .order_by("id")
        .all()
    )
    serializer_class = serializers.PortfolioSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True)
    def sectors(self, request, pk=None):
        investments = self.get_object().investments.all()

        sectors_data = []
        for sector in sorted(
            investments.values_list("asset__sector", flat=True).distinct()
        ):
            sector_investments = investments.filter(asset__sector=sector).all()

            invested_amounts = [
                investment.amount
                * investment.asset.historic_values.order_by("date_time").last().value
                for investment in sector_investments
            ]

            sectors_data.append(
                {
                    "sector": sector,
                    "total_invested": sum(invested_amounts),
                }
            )

        return Response(sectors_data)
