from django.contrib import admin
from .models import Item, Category, OrderItem, Order
# Register your models here.

admin.site.register(Item)
admin.site.register(Category)
admin.site.register(OrderItem)
admin.site.register(Order)