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


def signup(request):
    #функция регистрации
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('accounts/profile/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})





