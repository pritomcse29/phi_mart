from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin
from order.models import Cart,CartItem,Order
from order.serializers import updateOrderSerializer,CreateOrderSerializer,UpdateCartItemSerializer,AddCartItemSerializer,CartSerializer,CartItemSerializer,OrderSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
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
      
      # queryset = Order.objects.all()
      # serializer_class = OrderSerializer
      # permission_classes = [IsAuthenticated]
      http_method_names =['get','post','delete','patch','head','options']
      def get_permissions(self):
            if self.request.method == 'DELETE':
                  return [IsAdminUser()]
            return [IsAuthenticated()]
      # def get_permissions(self):
      #       if self.request.method  in ['PATCH', 'DELETE']:
      #             return [IsAdminUser()]
      #       return [IsAuthenticated()]
      
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
        return Response({'status': f'Order status updated to {request.data['status']}'})

      def get_serializer_class(self):
            if self.request.method =='POST':
                  return CreateOrderSerializer
            elif self.request.method =='PATCH':
                  return updateOrderSerializer
            return OrderSerializer
      def get_serializer_context(self):
            return {'user_id':self.request.user.id, 'user': self.request.user}
      def get_queryset(self):
            if getattr(self, 'swagger_fake_view', False):  # Avoid issues in schema generation
                  return Order.objects.none()
            if self.request.user.is_staff:
                  return Order.objects.prefetch_related('items__product').all()
            return Order.objects.prefetch_related('items__product').filter(user=self.request.user)