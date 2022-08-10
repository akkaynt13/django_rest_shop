from django.contrib import admin

from shop.views import *
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'item', ItemViewSet)
router.register(r'order', OrderViewSet)


urlpatterns = [
    #админка
    path('admin/', admin.site.urls),
    #отображение каталога, товаров и заказов
    path('', include(router.urls)),
    #отображение заказов авторизованного пользователя+добавление
    path('user_orders/', UserOrdersView.as_view({'get': 'list', 'post': 'create'})),
    #отображение отдельного заказа по номеру заказа (не pk)
    path('user_orders/<int:order_number>/', UserOrderView.as_view()),
    #изменение статуса заказа админом, заказ по pk
    path('user_orders/update/<int:pk>/', OrderStatusUpdate.as_view()),
    #auth/login
    path('auth/', include('rest_framework.urls')),
    #переопределение пути для отображения заказов пользователя после регистрации
    path('accounts/profile/', UserOrdersView.as_view({'get': 'list', 'post': 'create'})),
    #регистрация
    path('register', signup)
]
