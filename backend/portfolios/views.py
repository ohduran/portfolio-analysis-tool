from portfolios.models import Portfolio
from portfolios.serializers import PortfolioSerializer
from rest_framework import permissions, viewsets


class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = (
        Portfolio.objects.active()
        .prefetch_related("investments")
        .prefetch_related("investments__asset")
        .order_by("id")
        .all()
    )
    serializer_class = PortfolioSerializer
    permission_classes = [permissions.IsAuthenticated]
