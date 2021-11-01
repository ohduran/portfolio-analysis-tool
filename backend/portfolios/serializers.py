from rest_framework import serializers

from .models import Investment, Portfolio


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = (
            "id",
            "amount",
            "asset",
        )

    asset = serializers.StringRelatedField(many=False)


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = (
            "id",
            "name",
            "investments",
        )

    investments = InvestmentSerializer(many=True)
