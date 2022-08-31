from urllib import request
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from rest_framework import viewsets, generics
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy
from rest_framework.views import APIView
from shop.templates import *
from .permissions import IsAdminOrReadOnly
from .serializers import *
from . import models as m
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST


class ItemViewSet(viewsets.ModelViewSet):
    """
    Отображение всех товаров с возможностью добавления и редактирования для администратора
    """
    permission_classes = (IsAdminOrReadOnly, )
    queryset = m.Item.objects.all()
    serializer_class = ItemSerializer


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    # Отображение всез заказов
    queryset = m.Order.objects.all()
    serializer_class = OrderSerializer


class UserOrdersView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    # Отображение всех заказов авторизованного пользователя с возможностью добавления

    def get_queryset(self):
        return m.Order.objects.filter(user=self.request.user)


class UserOrderView(APIView):
    # Отображение заказа авторизованного пользователя по номеру заказа
    permission_classes = (IsAuthenticated, )

    def get(self, request, order_number):
        orders = m.Order.objects.filter(
            user=self.request.user).filter(order_number=order_number)
        return Response(OrdersViewSerializer(orders, many=True).data)


class OrderStatusUpdate(generics.RetrieveUpdateAPIView):
    # Изменение статуса заказа администратором по pk заказа
    queryset = m.Order.objects.all()
    serializer_class = OrdersViewSerializer
    permission_classes = (IsAdminUser, )


@api_view(['POST'])
def signup(request):
    data = {
        'username': request.data.get('name'),
        'password': request.data.get('password')
    }
    serializer = RegisterUserSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        
