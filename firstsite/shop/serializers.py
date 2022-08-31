from rest_framework import serializers

from . import models as m


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Item
        fields = ('name', 'price', 'amount')


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.HiddenField(default='Created')
    items = serializers.PrimaryKeyRelatedField(queryset=m.Item.objects.all())
    class Meta:
        model = m.Order
        fields = '__all__'



class OrdersViewSerializer(serializers.Serializer):
    order_number = serializers.IntegerField(read_only=True)
    status = serializers.ChoiceField(choices=m.Order.status_choices)
    items = serializers.CharField(read_only=True)
    count = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        return m.Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

class RegisterUserSerializer(serializers.ModelSerializer): #переименовать в signup
    class Meta:
        model = m.User
        fields = ('username', 'password', )
        

