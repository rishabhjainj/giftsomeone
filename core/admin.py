from django.contrib import admin
from .models import Product, OrderProduct, Order, Category, Label

# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Category)
admin.site.register(Label)
