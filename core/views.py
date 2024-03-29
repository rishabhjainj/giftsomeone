from django.shortcuts import render
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth import authenticate, login as auth_login
from paytmchecksum import PaytmChecksum
from django.utils import timezone
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer



# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['get'], )
    def get_wishlist(self, request, pk=None):
        queryset = WishList.objects.all().filter(owner=request.user.pk)
        serializer = WishListSerializer(queryset, many=True)
        return Response(serializer.data)

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
                wishlist_product_queryset = wishList.products.filter(product=product)
                if wishlist_product_queryset.exists():
                    print(product.id)
                    return Response({'wishList': 'Product already in wishlist'})
                else:
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


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated, )

    def list(self, request):
        queryset = Transaction.objects.all().filter(made_by=request.user)
        serializer = TransactionSerializer(queryset, many=True)
        return Response(serializer.data)


class BillingAddressViewSet(viewsets.ModelViewSet):
    queryset = BillingAddress.objects.all()
    serializer_class = WishListSerializer
    permission_classes = (IsAuthenticated, )

    def list(self, request):
        queryset = BillingAddress.objects.all().filter(owner=request.user)
        serializer = BillingAddressSerializer(queryset, many=True)
        return Response(serializer.data)

@csrf_exempt
@api_view(('POST', 'GET',))
def initiate_payment(request):
    if request.method == "GET":
        return render(request, 'core/pay.html')
    order_id = request.POST['order_id']
    if request.method == "GET":
        return TransactionViewSet
    try:
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is None:
            raise ValueError
        auth_login(request=request, user=user)
        order = Order.objects.get(pk=order_id)
        amount = order.amount
        transaction = Transaction.objects.create(made_by=request.user, amount=amount, order=order)
        transaction.save()
        merchant_key = settings.PAYTM_SECRET_KEY
        params = (
           ('MID', settings.PAYTM_MERCHANT_ID),
           ('ORDER_ID', str(transaction.order_id)),
           ('CUST_ID', str(transaction.made_by.email)),
           ('TXN_AMOUNT', str(transaction.amount)),
           ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
           ('WEBSITE', settings.PAYTM_WEBSITE),
           ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
           ('CALLBACK_URL', 'http://localhost:8002/api/callback/'),
        )
        paytm_params = dict(params)
        checksum = PaytmChecksum.generateSignature(paytm_params, merchant_key)
        transaction.checksum = checksum
        transaction.save()
        paytm_params['CHECKSUMHASH'] = checksum
        print(paytm_params)
        print('SENT', checksum)
        return render(request, 'core/redirect.html', context=paytm_params)
    except Exception as e:
       print("error")
       print(e)
       return Response({'payments': 'error'})

@csrf_exempt
def callback(request):
    received_data = dict(request.POST)
    paytm_params = {}
    print("recieved data:")
    print(request.POST)
    paytm_checksum = received_data['CHECKSUMHASH'][0]
    # transaction_id = received_data['TRANSACTION_ID'][0]
    # transaction_query = Transaction.objects.filter(transaction_id=transaction_id)
    # transaction = transaction_query[0]

    for key, value in received_data.items():
        if key == 'CHECKSUMHASH':
            paytm_checksum = value[0]
        else:
            paytm_params[key] = str(value[0])
    # Verify checksum
    is_valid_checksum = PaytmChecksum.verifySignature(paytm_params, settings.PAYTM_SECRET_KEY, paytm_checksum)
    if is_valid_checksum:
        # transaction.status = "Success"
        # transaction.save()
        received_data['message'] = "Checksum Matched"
    else:
        # transaction.status = "Failed"
        # transaction.save()
        received_data['message'] = "Checksum Mismatched"
        return render(request, 'core/callback.html', context=received_data)

    return render(request, 'core/callback.html', context=received_data)


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
                order.save()
                return Response({'product': 'Product removed successfully'})

            else:
                return Response({'product_id': 'Product id is invalid'})
        except Exception as e:
            print(e)
            return Response({'order_id': 'Order id is invalid'})


    @action(detail=True, methods=['post'], )
    def checkout(self, request, pk=None):
        order_query_set = Order.objects.all().filter(owner=request.user, ordered=False)
        if order_query_set.exists():
            order = order_query_set[0]
            street_address = request.data.get('street_address')
            apartment_address = request.data.get('apartment_address')
            country = request.data.get('country')
            state = request.data.get('state')
            zip_code = request.data.get('zip')
            amount = request.data.get('amount')
            billing_address = BillingAddress(
                owner=self.request.user,
                street_address=street_address,
                apartment_address=apartment_address,
                country=country,
                state=state,
                zip=zip_code
            )
            billing_address.save()
            order.amount = amount
            order.billing_address = billing_address
            order.ordered = True
            order.status = 'paid'
            order.order_date = timezone.now()

            order.save()
            return Response({'order': 'Order placed successfully'})
        else:
            return Response({'order': 'No active orders found'})

    @action(detail=True, methods=['get'], )
    def get_cart(self, request, pk=None):
        queryset = Order.objects.all().filter(owner=request.user.pk, ordered=False)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'],)
    def add_to_cart(self, request, pk=None):
        product_id = request.data.get('product', None)
        qty = request.data.get('qty', None)
        print(qty)
        if product_id is None:
            return Response({'product': 'Product is required'})
        try:
            product = Product.objects.get(pk=product_id)
            order_query_set = Order.objects.all().filter(owner=request.user, ordered=False)
            if order_query_set.exists():
                print("exitsts")
                order = order_query_set[0]
                if order.products.filter(product=product).exists():
                    order_product = order.products.filter(product=product)[0]
                    if qty is None:
                        order_product.quantity += 1
                    elif qty == 0:
                        print("deleting")
                        OrderProduct.objects.all().filter(pk=order_product.id).delete()
                        order.save()
                        return Response({'cart': 'Product removed'})
                    else:
                        print("not zero")
                        order_product.quantity += qty
                    print(order_product.quantity)
                    order_product.save()
                else:
                    if qty is None:
                        order.products.add(OrderProduct.objects.create(product=product))
                    else:
                        order.products.add(OrderProduct.objects.create(product=product, quantity=qty))
            else:
                ordered_date = timezone.now()
                order = Order.objects.create(owner=request.user, order_date=ordered_date)
                if qty is None:
                    order.products.add(OrderProduct.objects.create(product=product))
                else:
                    order.products.add(OrderProduct.objects.create(product=product, quantity=qty))
            order.save()
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






