from rest_framework import serializers
from .models import Customer, StoneItem


class DealSerializer(serializers.Serializer):
    file = serializers.FileField()


class StoneItemSerializer(serializers.ModelSerializer):

    stone = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = StoneItem
        fields = ['stone']


class CustomerSerializer(serializers.ModelSerializer):

    stones = StoneItemSerializer(many=True)

    class Meta:
        model = Customer
        fields = ['username', 'spent_money', 'stones']
