from assets.models import Asset
from django.db import transaction
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

    asset = serializers.SlugRelatedField(
        slug_field="symbol", queryset=Asset.objects.all()
    )


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = (
            "id",
            "name",
            "investments",
        )

    investments = InvestmentSerializer(many=True)

    def validate(self, data):
        data["user"] = self.context["request"].user
        return super().validate(data)

    def create(self, validated_data):
        investments = validated_data.pop("investments")
        with transaction.atomic():
            portfolio = super().create(validated_data)
            for investment_data in investments:
                Investment.objects.create(portfolio=portfolio, **investment_data)
        return portfolio
