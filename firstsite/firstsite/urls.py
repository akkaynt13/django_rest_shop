from django.contrib import admin

from shop.views import *
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'item', ItemViewSet)
router.register(r'order', OrderViewSet)


urlpatterns = [
    path('admin/', admin.site.urls), #админка
    path('', include(router.urls)), #отображение каталога, товаров и заказов
    path('user_orders/', UserOrdersView.as_view({'get': 'list', 'post': 'create'})), #отображение заказов авторизованного пользователя+добавление
    path('user_orders/<int:order_number>/', UserOrderView.as_view()), #отображение отдельного заказа по номеру заказа (не pk)
    path('user_orders/update/<int:pk>/', OrderStatusUpdate.as_view()), #изменение статуса заказа админом, заказ по pk
    path('auth/', include('rest_framework.urls'), name='login'),
    path('accounts/profile/', UserOrdersView.as_view({'get': 'list', 'post': 'create'})),
    path('register', signup)
]
