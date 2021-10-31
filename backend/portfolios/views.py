from portfolios.models import Portfolio
from portfolios.serializers import PortfolioSerializer
from rest_framework import permissions, viewsets


class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = [permissions.IsAuthenticated]
