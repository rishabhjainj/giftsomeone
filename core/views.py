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
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['post'], )
    def add_to_wishlist(self, request, pk=None):
        if pk is None:
            return Response({'product': 'Product is required'})
        else:
            product = Product.objects.get(pk=pk)
        try:
            wishlist_query_set = WishList.objects.all().filter(owner=request.user)
            if wishlist_query_set.exists():
                wishList = wishlist_query_set[0]
                wishListProduct = WishListProduct.objects.create(product=product)
                wishList.products.add(wishListProduct)
                wishList.save()
            else:
                wishList = WishList.objects.create(owner=request.user)
                wishListProduct = WishListProduct.objects.create(product=product)
                wishList.products.add(wishListProduct)
                wishList.save()
            return Response({'wishList': 'Product added Successfully'})
        except Exception as e:
            print(e)
            return Response({'product_id': 'product does not exist'})

    @action(detail=True, methods=['post'], )
    def remove_from_wishlist(self, request, pk=None):
        if pk is None:
            return Response({'product': 'Product is required'})
        else:
            product = Product.objects.get(pk=pk)
        try:
            wishlist_query_set = WishList.objects.all().filter(owner=request.user)
            if wishlist_query_set.exists():
                wishList = wishlist_query_set[0]
                wishlist_products = wishList.products.filter(product=product)
                if wishlist_products.exists():
                    product_to_remove = wishlist_products[0]
                    WishListProduct.objects.filter(pk=product_to_remove.id).delete()
                    return Response({'wishlist': 'Product removed successfully.'})
                else:
                    return Response({'wishlist': 'Product does not exists'})

            else:
                return Response({'wishlist': 'No wishlist exists.'})
        except Exception as e:
            print(e)
            return Response({'product_id': 'product does not exist'})


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelsSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class WishListViewSet(viewsets.ModelViewSet):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = (IsAuthenticated, )

    def list(self, request):
        queryset = WishList.objects.all().filter(owner=request.user)
        serializer = WishListSerializer(queryset, many=True)
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, )

    @action(detail=True, methods=['post'], )
    def remove_from_cart(self, request, pk=None):
        product_id = request.data.get('product', None)
        if product_id is None:
            return Response({'product': 'Product is required'})
        try:
            order = Order.objects.get(pk=pk)
            product = Product.objects.get(pk=product_id)
            if order is None:
                return Response({'order_id': 'Order id is invalid'})
            if order.products.filter(product=product).exists():
                order_product = order.products.filter(product=product)[0]
                if order_product.quantity == 1:
                    OrderProduct.objects.filter(pk=order_product.id).delete()
                else:
                    order_product.quantity -= 1
                    order_product.save()
                return Response({'product': 'Product removed successfully'})

            else:
                return Response({'product_id': 'Product id is invalid'})
        except Exception as e:
            print(e)
            return Response({'order_id': 'Order id is invalid'})

    @action(detail=True, methods=['post'],)
    def add_to_cart(self, request, pk=None):
        product_id = request.data.get('product', None)
        if product_id is None:
            return Response({'product': 'Product is required'})
        try:
            product = Product.objects.get(pk=product_id)
            order_query_set = Order.objects.all().filter(owner=request.user, ordered=False)
            if order_query_set.exists():
                order = order_query_set[0]
                if order.products.filter(product=product).exists():
                    order_product = order.products.filter(product=product)[0]
                    order_product.quantity += 1
                    order_product.save()
                else:
                    order.products.add(OrderProduct.objects.create(product=product))
            else:
                ordered_date = timezone.now()
                order = Order.objects.create(owner=request.self, order_date=ordered_date)
                order.products.add(OrderProduct.objects.create(product=product))
            return Response({'product': 'Product added successfully'})

        except Exception as e:
            print(e)
            return Response({'product': 'Invalid product id provided'})

    # def perform_create(self, serializer):
    #     serializers.save(owner=self.request.user)

    def list(self, request):
        queryset = Order.objects.all().filter(owner=request.user.pk)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)




