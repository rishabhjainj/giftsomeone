from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(required=False)

    class Meta:
        model = OrderProduct
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, required=False)

    class Meta:
        model = Category
        fields = '__all__'


class BillingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingAddress
        fields = '__all__'


class LabelsSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, required=False)

    class Meta:
        model = Label
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, required=False)
    payment = TransactionSerializer(many=True, required=False)
    billing_address = BillingAddressSerializer(required=False)

    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {'owner': {'required': True}}


class WishListProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(required=False)

    class Meta:
        model = WishListProduct
        fields = '__all__'


class WishListSerializer(serializers.ModelSerializer):
    products = WishListProductSerializer(many=True, required=False)

    class Meta:
        model = WishList
        fields = '__all__'
        extra_kwargs = {'owner': {'required': True}}
