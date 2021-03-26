from django.db import models
from giftSomeone.helpers import PathAndRenameFile
from giftSomeone import settings
from django.shortcuts import reverse
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=PathAndRenameFile('categories'), null=True, blank=True)

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    label = models.ForeignKey(Label, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    unit_weight = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to=PathAndRenameFile('products'), null=True, blank=True)
    units_in_stock = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.title


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"


class Order(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField(OrderProduct)
    order_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    discount = models.IntegerField()

    def __str__(self):
        return self.owner.email


class WishListProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.title


class WishList(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wishlist")
    products = models.ManyToManyField(WishListProduct)

    def __str__(self):
        return self.owner.email

