from django.contrib.auth.models import User
from django.db import models


class Item(models.Model):
    name = models.CharField('имя', max_length=20, default='')
    price = models.PositiveIntegerField('цена', blank=True)
    amount = models.PositiveIntegerField('количество на складе', blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    status_choices = (
        ('Created', 'Created'),
        ('Payed', 'Payed'),
        ('Sent', 'Sent'),
        ('Received', 'Received')
    )
    order_number = models.PositiveIntegerField('Номер заказа')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField('статус заказа',
                              max_length=8,
                              choices=status_choices,
                              default='Created')
    items = models.ForeignKey('Item', on_delete=models.DO_NOTHING)
    count = models.PositiveIntegerField()


