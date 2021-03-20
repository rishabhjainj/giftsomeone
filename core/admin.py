from django.contrib import admin
from .models import Product, OrderProduct, Order

# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderProduct)

