from django.contrib import admin

from shop.views import *
from django.urls import path, include

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'item', ItemViewSet)
router.register(r'order', OrderViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('user_orders/', UserOrdersView.as_view({'get': 'list', 'post': 'create'})),
    path('user_orders/<int:order_number>/', UserOrderView.as_view()),
    path('user_orders/update/<int:pk>/', OrderStatusUpdate.as_view())
]
