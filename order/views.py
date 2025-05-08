from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin
from order.models import Cart,CartItem,Order
from order.serializers import updateOrderSerializer,CreateOrderSerializer,UpdateCartItemSerializer,AddCartItemSerializer,CartSerializer,CartItemSerializer,OrderSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from order.services import OrderService
from order import serializers as orderSz
from rest_framework.decorators import api_view
from sslcommerz_lib import SSLCOMMERZ 
class CartViewSet(CreateModelMixin,DestroyModelMixin,RetrieveModelMixin,GenericViewSet):
      
      # queryset = Cart.objects.all()
      serializer_class = CartSerializer
      permission_classes = [IsAuthenticated]
      def perform_create(self, serializer):
            serializer.save(user=self.request.user)
      def get_queryset(self):
            if getattr(self, 'swagger_fake_view', False):  # Avoid issues in schema generation
                  return Cart.objects.none()
            if self.request.user.is_authenticated:
               return Cart.objects.filter(user=self.request.user)
            return Cart.objects.none()  # Return empty queryset for anonymous users
      def create(self, request,*args, **kwargs):
            existing_cart = Cart.objects.filter(user=request.user).first()
            if existing_cart:
                  serializer = self.get_serializer(existing_cart)
                  return Response(serializer.data, status=status.HTTP_200_OK)
            return super().create(request, *args, **kwargs)
            # return Cart.objects.filter(user=self.request.user)
# class CartItemViewSet(ModelViewSet):
#     queryset = CartItem.objects.all()
#     serializer_class = CartItemSerializer

#     def get_queryset(self):
#         # This is to handle swagger schema generation and avoid KeyError
#         if getattr(self, 'swagger_fake_view', False):
#             return CartItem.objects.none()  # Avoid errors during schema generation
        
#         # Safely access 'cart_pk' using .get() to avoid KeyError
#         cart_pk = self.kwargs.get('cart_pk')  
        
#         if cart_pk:
#             return CartItem.objects.filter(cart_id=cart_pk)
        
#         return CartItem.objects.none()  # Return empty queryset if 'cart_pk' is missing


# class CartItemViewSet(ModelViewSet):
#       queryset = CartItem.objects.all()
#       serializer_class = CartItemSerializer

#       def get_queryset(self):
#             if getattr(self,'swagger_fake_view', False):
#                   return CartItem.objects.none()
#             return CartItem.objects.filter(cart_id =  self.kwargs['cart_pk'])
class CartItemViewSet(ModelViewSet):
      http_method_names =['get','post','delete','patch']
    #   queryset = CartItem.objects.all()
      serializer_class = CartItemSerializer
      def get_serializer_class(self):
            if self.request.method == 'POST':
                  return AddCartItemSerializer
            elif self.request.method == 'PATCH':
                return UpdateCartItemSerializer
            return CartItemSerializer
      def get_serializer_context(self):
            return {'cart_id':self.kwargs.get('cart_pk')}
      def get_queryset(self):
            return CartItem.objects.filter(cart_id=self.kwargs.get('cart_pk'))
class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'patch', 'head', 'options']

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        OrderService.cancel_order(order=order, user=request.user)
        return Response({'status': 'Order canceled'})

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        serializer = orderSz.UpdateOrderSerializer(
            order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': f"Order status updated to {request.data['status']}"})

    def get_permissions(self):
        if self.action in ['update_status', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'cancel':
            return orderSz.EmptySerializer
        if self.action == 'create':
            return orderSz.CreateOrderSerializer
        elif self.action == 'update_status':
            return orderSz.UpdateOrderSerializer
        return orderSz.OrderSerializer

    def get_serializer_context(self):
        if getattr(self, 'swagger_fake_view', False):
            return super().get_serializer_context()
        return {'user_id': self.request.user.id, 'user': self.request.user}

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items__product').all()
        return Order.objects.prefetch_related('items__product').filter(user=self.request.user)
# class OrderViewSet(ModelViewSet):
      
#       # queryset = Order.objects.all()
#       # serializer_class = OrderSerializer
#       # permission_classes = [IsAuthenticated]
#       http_method_names =['get','post','delete','patch','head','options']
#       def get_permissions(self):
#             if self.request.method == 'DELETE':
#             # if self.request.method == ['PATCH','DELETE']:
#                   return [IsAdminUser()]
#             return [IsAuthenticated()]
#       # def get_permissions(self):
#       #       if self.request.method  in ['PATCH', 'DELETE']:
#       #             return [IsAdminUser()]
#       #       return [IsAuthenticated()]
      
#       @action(detail=True, methods=['post'])
#       def cancel(self, request, pk=None):
#             order = self.get_object()
#             OrderService.cancel_order(order=order, user=request.user)
#             return Response({'status': 'Order canceled'})

#       @action(detail=True, methods=['patch'])
#       def update_status(self, request, pk=None):
#             order = self.get_object()
#             serializer = updateOrderSerializer(
#                   order, data=request.data, partial=True)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response({"status": f"Order status updated to {request.data['status']}"})


#       def get_serializer_class(self):
#             if self.request.method =='POST':
#                   return CreateOrderSerializer
#             elif self.request.method =='PATCH':
#                   return updateOrderSerializer
#             return OrderSerializer
#       def get_serializer_context(self):
#             return {'user_id':self.request.user.id, 'user': self.request.user}
#       def get_queryset(self):
#             if getattr(self, 'swagger_fake_view', False):  # Avoid issues in schema generation
#                   return Order.objects.none()
#             if self.request.user.is_staff:
#                   return Order.objects.prefetch_related('items__product').all()
#             return Order.objects.prefetch_related('items__product').filter(user=self.request.user)

@api_view(['POST'])
def initiate_payment(request):
    user = request.user
    amount = request.data.get("amount") 
    order_id = request.data.get("orderId")   
    num_items = request.data.get("numItems")
    settings = { 'store_id': 'tesphima681cdd5d122b5', 'store_pass': 'phima681cdd5d122b5@ssl', 'issandbox': True }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = f"txn_{order_id}"
    post_body['success_url'] = "http://localhost:5173/dashboard/payment/success/"
    post_body['fail_url'] = "http://localhost:5173/dashboard/payment/orders/"
    post_body['cancel_url'] = "http://localhost:5173/dashboard/orders/"
    post_body['emi_option'] = 0
    post_body['cus_name'] = f"{user.first_name} {user.last_name}"
    post_body['cus_email'] = user.email
    post_body['cus_phone'] = user.phone_number
    post_body['cus_add1'] = user.address
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "Courier"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = num_items
    post_body['product_name'] = "E-Commerce Products"
    post_body['product_category'] = "General"
    post_body['product_profile'] = "general"


    response = sslcz.createSession(post_body) # API response
    print(response)

    if response.get("status")=='SUCCESS':
       return Response({"payment_url":response['GatewayPageURL']})
    return Response({"error":"Payment initiation failed"},status=status.HTTP_400_BAD_REQUEST)
    # return Response(response)
    # Need to redirect user to response['GatewayPageURL']