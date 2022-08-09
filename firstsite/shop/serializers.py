from rest_framework import serializers

from . import models
from .models import Item, Order


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('name', 'price', 'amount')


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.HiddenField(default='Created')
    items = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    class Meta:
        model = Order
        fields = '__all__'



class OrdersViewSerializer(serializers.Serializer):
    order_number = serializers.IntegerField(read_only=True)
    status = serializers.ChoiceField(choices=models.Order.status_choices)
    items = serializers.CharField(read_only=True)
    #items = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    count = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


