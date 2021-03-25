from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer( required=False)

    class Meta:
        model = OrderProduct
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, required=False)

    class Meta:
        model = Category
        fields = '__all__'


class LabelsSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, required=False)

    class Meta:
        model = Label
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {'owner': {'required': True}}
