from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import  viewsets
from .serializers import *


# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializers.save(owner=self.request.user)

    # @action(detail=True, methods=('post', ), permission_classes=(IsAuthenticated, ) )
    # def add_product(self, request, pk):



