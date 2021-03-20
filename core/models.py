from django.db import models
from giftSomeone.helpers import PathAndRenameFile
from giftSomeone import settings
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    unit_weight = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to=PathAndRenameFile('products'), null=True, blank=True)
    units_in_stock = models.IntegerField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True, blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.IntegerField()


class Order(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField(OrderProduct)
    order_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.owner.email
