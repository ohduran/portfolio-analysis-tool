from portfolios import serializers
from portfolios.models import Portfolio
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = (
        Portfolio.objects.active()
        .prefetch_related("investments")
        .prefetch_related("investments__asset")
        .order_by("id")
        .all()
    )
    serializer_class = serializers.PortfolioSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True)
    def sectors(self, request, pk=None):
        portfolio = self.get_object()
        serializer = serializers.SectorPortfolioSerializer(portfolio)
        return Response(serializer.data)
