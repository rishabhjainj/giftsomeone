from django.db import models
from giftSomeone.helpers import PathAndRenameFile
from giftSomeone import settings
from django.db.models.signals import pre_save, post_save
from django.shortcuts import reverse
import binascii
import os
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
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def has_inventory(self):
        return self.units_in_stock > 0


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"


class BillingAddress(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='billing_address')
    street_address = models.CharField(max_length=255)
    apartment_address = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.owner.email


ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('stale', 'Stale'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    ('refunded', 'Refunded'),
)


class Order(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField(OrderProduct)
    order_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='created')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.IntegerField(default=0)
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.SET_NULL, blank=True, null=True,
                                        related_name='billing_address')

    def __str__(self):
        return self.owner.email

    def calculate(self, save=False):
        if not self.id:
            return {}
        if not self.products:
            return {}
        prod_sum = 0
        for order_product in self.products.all():
            try:
                product = order_product.product
                qty = order_product.quantity
                price = product.price
                discount = product.discount
                total_price = price - (price * discount/100)
                total_price = total_price*qty
                total_price = float("%.2f" % total_price)
                prod_sum += total_price
                prod_sum = float("%.2f" % prod_sum)
            except Exception as e:
                print(e)
        totals = {
            "amount": prod_sum
        }
        for k, v in totals.items():
            setattr(self, k, v)
            if save:
                self.save()
        return totals


def order_pre_save(sender, instance, *args, **kwargs):
    instance.calculate(save=False)


pre_save.connect(order_pre_save, sender=Order)


# def order_post_save(sender, instance, created, *args, **kwargs):
#     if created:
#         instance.calculate(save=True)
#
#
# post_save.connect(order_post_save, sender=Order)


class WishListProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.title


class WishList(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wishlist")
    products = models.ManyToManyField(WishListProduct)

    def __str__(self):
        return self.owner.email


class Transaction(models.Model):
    made_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="transactions", on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(default=0)
    transaction_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    order = models.ForeignKey(Order, related_name="payment", on_delete=models.CASCADE)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        print("saving")
        if self.transaction_id is None:
            try:
                self.transaction_id = binascii.hexlify(os.urandom(32)).decode()+str(self.order)
                # print(self.transaction_id)
                return super().save(*args, **kwargs)
            except Exception as e:
                print(e)
        else:
            return super().save(*args, **kwargs)

