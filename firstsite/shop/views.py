from rest_framework import viewsets, generics
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsAdminOrReadOnly
from .serializers import *


class ItemViewSet(viewsets.ModelViewSet):
    #Отображение всех товаров с возможностью добавления и редактирования для администратора
    permission_classes = (IsAdminOrReadOnly, )
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    #Отображение всез заказов
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class UserOrdersView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    #Отображение всех заказов авторизованного пользователя с возможностью добавления
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class UserOrderView(APIView):
    #Отображение заказа авторизованного пользователя по номеру заказа
    permission_classes = (IsAuthenticated, )
    def get(self, request, order_number):
        orders = Order.objects.filter(user=self.request.user).filter(order_number=order_number)
        return Response(OrdersViewSerializer(orders, many=True).data)


class OrderStatusUpdate(generics.RetrieveUpdateAPIView):
    #Изменение статуса заказа администратором по pk заказа
    queryset = Order.objects.all()
    serializer_class = OrdersViewSerializer
    permission_classes = (IsAdminUser, )










