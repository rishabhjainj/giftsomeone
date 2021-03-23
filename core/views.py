from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import *
from django.utils import timezone


# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelsSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, )

    def list(self, request):
        queryset = Order.objects.all().filter(owner=request.user)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=('post',), permission_classes=(IsAuthenticated,), )
    def add_to_cart(self, request, pk):
        product_id = request.data.get('product', None)
        if product_id is None:
            return Response({'product': 'Product is required'})
        try:
            product = Product.objects.get(pk=product_id)
            order_product = OrderProduct.objects.create(product=product)
            order_query_set = Order.objects.all().filter(owner=request.user, ordered=False)
            if order_query_set.exists():
                order = order_query_set[0]
                if order.products.filter(pk=product_id).exists():
                    order_product.quantity += 1
                    order_product.save()
                else:
                    order.products.add(order_product)
            else:
                ordered_date = timezone.now()
                order = Order.objects.create(owner=request.self, order_date=ordered_date)
                if order.products.filter(pk=product_id).exists():
                    order_product.quantity += 1
                    order_product.save()
                else:
                    order.products.add(order_product)
            return Response({'product': 'Product added successfully'})

        except Exception as e:
            return Response({'product': 'Invalid product id provided'})

    def perform_create(self, serializer):
        serializers.save(owner=self.request.user)



