from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from product.models import Product, Category, Review, ProductImage
from product.serializers import ProductSerializer, CategorySerializer, ReviewSerializer, ProductImageSerializer
from product.permissions import IsAdminOrReadOnly
from product.filters import ProductFilter
from product.paginations import DefaultPagination


class ProductViewSet(ModelViewSet):
    """
    API endpoint for managing products in the e-commerce store.
    """
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'updated_at']
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination

    def get_queryset(self):
        return Product.objects.select_related('category').prefetch_related('images').all()

    @swagger_auto_schema(
        operation_summary='Retrieve a list of products',
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="Search by name or description", type=openapi.TYPE_STRING),
            openapi.Parameter('ordering', openapi.IN_QUERY, description="Order by price or updated_at", type=openapi.TYPE_STRING),
            openapi.Parameter('category_id', openapi.IN_QUERY, description="Filter by category ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('price__gt', openapi.IN_QUERY, description="Minimum price", type=openapi.TYPE_NUMBER),
            openapi.Parameter('price__lt', openapi.IN_QUERY, description="Maximum price", type=openapi.TYPE_NUMBER),
        ]
    )
    def list(self, request, *args, **kwargs):
        """Retrieve all the products"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a product by admin",
        operation_description="This allows an admin to create a product",
        request_body=ProductSerializer,
        responses={201: ProductSerializer, 400: "Bad Request"}
    )
    def create(self, request, *args, **kwargs):
        """Only authenticated admin can create a product"""
        return super().create(request, *args, **kwargs)


class ProductImageViewSet(ModelViewSet):
    """
    Handles image uploads for a specific product.
    """
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs.get('product_pk'))

    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs.get('product_pk'))


class CategoryViewSet(ModelViewSet):
    """
    Manages product categories.
    """
    queryset = Category.objects.annotate(product_count=Count('products')).all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class ReviewViewSet(ModelViewSet):
    """
    Handles reviews for a specific product.
    """
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs.get('product_pk'))

    def get_serializer_context(self):
        return {'product_id': self.kwargs.get('product_pk')}

# from django.shortcuts import render
# from django.http import HttpResponse
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from product.models import Product,Category,Review,ProductImage
# from rest_framework import status
# from django.shortcuts import get_object_or_404
# from product.serializers import ProductImageSerializer,ProductSerializer,CategorySerializer, ReviewSerializer
# from django.db.models import Count
# from rest_framework.views import APIView
# from rest_framework.generics import ListCreateAPIView
# from rest_framework.generics import RetrieveUpdateDestroyAPIView
# from rest_framework.viewsets import ModelViewSet
# from django_filters.rest_framework import DjangoFilterBackend
# from product.filters import ProductFilter
# from rest_framework.filters import OrderingFilter, SearchFilter
# from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
# # from rest_framework import permissions
# from product.permissions import IsAdminOrReadOnly
# from rest_framework.permissions import DjangoModelPermissions,DjangoModelPermissionsOrAnonReadOnly
# from drf_yasg.utils import swagger_auto_schema
# # from rest_framework.pagination import PageNumberPagination
# from product.paginations import DefaultPagination
# from drf_yasg import openapi
# # from api.permissions import IsAdminOrReadOnly, FullDjangoModelPermission
# # # Create your views here.
# class ProductViewSet(ModelViewSet):
#       """
#     API endpoint for managing products in the e-commerce store
#      - Allows authenticated admin to create, update, and delete products
#      - Allows users to browse and filter product
#      - Support searching by name, description, and category
#      - Support ordering by price and updated_at
#     """
      
#       # queryset = Product.objects.all()
#       serializer_class = ProductSerializer
#       filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    
#       filterset_class = ProductFilter
#       search_fields = ['name', 'description',]
#       ordering_fields = ['price','updated_at']
#       permission_classes = [IsAdminOrReadOnly]
#       pagination_class = DefaultPagination
#      #  permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
#      #  permission_classes = [DjangoModelPermissions]
      
#      #  permission_classes = [IsAdminUser]
#      #  def get_permissions(self):
#      #       if self.request.method == "GET":
#      #            return [AllowAny()]
#      #       return[IsAdminUser()]

#        #  filterset_fields = ['category_id','price']
#      #  def get_queryset(self):
#      #       queryset = Product.objects.all()
#      #       category_id = self.request.query_params.get('category_id')
#      #       if category_id is not None:
#      #            queryset = Product.objects.filter(category_id=category_id)

#      #       return queryset   
#      #  
#     #   @swagger_auto_schema(
#     #     manual_parameters=[
#     #         openapi.Parameter('search', openapi.IN_QUERY, description="Search by name or description", type=openapi.TYPE_STRING),
#     #         openapi.Parameter('ordering', openapi.IN_QUERY, description="Order by price or updated_at", type=openapi.TYPE_STRING),
#     #         openapi.Parameter('category_id', openapi.IN_QUERY, description="Filter by category (exact match)", type=openapi.TYPE_INTEGER),
#     #         openapi.Parameter('price__gt', openapi.IN_QUERY, description="Minimum price", type=openapi.TYPE_NUMBER),
#     #         openapi.Parameter('price__lt', openapi.IN_QUERY, description="Maximum price", type=openapi.TYPE_NUMBER),
#     #     ]
#     # )
#       def get_queryset(self):
#         return Product.objects.prefetch_related('images').all()
 
#     #   @swagger_auto_schema(
#     #   operation_summary='Retrive a list of products'
#     # )
#     #   def list(self, request, *args, **kwargs):
#     #     """Retrive all the products"""
#     #     return super().list(request, *args, **kwargs)
#     @swagger_auto_schema(
#       operation_summary='Retrieve a list of products',
#       manual_parameters=[
#         openapi.Parameter('search', openapi.IN_QUERY, description="Search by name or description", type=openapi.TYPE_STRING),
#         openapi.Parameter('ordering', openapi.IN_QUERY, description="Order by price or updated_at", type=openapi.TYPE_STRING),
#         openapi.Parameter('category_id', openapi.IN_QUERY, description="Filter by category ID", type=openapi.TYPE_INTEGER),
#         openapi.Parameter('price__gt', openapi.IN_QUERY, description="Minimum price", type=openapi.TYPE_NUMBER),
#         openapi.Parameter('price__lt', openapi.IN_QUERY, description="Maximum price", type=openapi.TYPE_NUMBER),
#       ]
#      )
#       def list(self, request, *args, **kwargs):
#          """Retrieve all the products"""
#           return super().list(request, *args, **kwargs)


#       @swagger_auto_schema(
#         operation_summary="Create a product by admin",
#         operation_description="This allow an admin to create a product",
#         request_body=ProductSerializer,
#         responses={
#             201: ProductSerializer,
#             400: "Bad Request"
#         }
#     )
     
#       def create(self, request, *args, **kwargs):
#         """Only authenticated admin can create product"""
#         return super().create(request, *args, **kwargs)
      
#      #  def destroy(self, request, *args, **kwargs):
#      #       product =  self.get_object()
#      #       if product.stock >10 :
#      #            return Response({'message':"Product with stock more than 10 could not be deleted"})
#      #       self.perform_destroy(product)
#      #       return Response(status=status.HTTP_204_NO_CONTENT)

# class ProductImageViewSet(ModelViewSet):
#     serializer_class = ProductImageSerializer

#     def get_queryset(self):
#      #    if getattr(self, 'swagger_fake_view', False):  
#      #        return ProductImage.objects.none()  
        
#      #    product_pk = self.kwargs.get('product_pk')  
#      #    if product_pk:
#             return ProductImage.objects.filter(product_id=self.kwargs.get('product_pk'))
#      #    return ProductImage.objects.none()

#     def perform_create(self, serializer):
#         serializer.save(product_id = self.kwargs.get('product_pk'))
#      #    product_pk = self.kwargs.get('product_pk')  
#      #    if product_pk:
#      #        serializer.save(product_id=product_pk)

# # class ProductImageViewSet(ModelViewSet):
# #      serializer_class = ProductImageSerializer
# #      def get_queryset(self):
# #           return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])
# #      def perform_create(self, serializer):
# #           serializer.save(product_id = self.kwargs.get['product_pk'])
          
# class CategoryViewSet(ModelViewSet):
#      queryset = Category.objects.annotate(
#           product_count = Count('products')).all()
#      serializer_class = CategorySerializer
#      permission_classes = [IsAdminOrReadOnly]
#      # permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
# # class ReviewViewSet(ModelViewSet):
# #     serializer_class = ReviewSerializer

# #     def get_queryset(self):
# #         if getattr(self, 'swagger_fake_view', False):  
# #             return Review.objects.none()  
        
# #         product_pk = self.kwargs.get('product_pk')  
# #         if product_pk:
# #             return Review.objects.filter(product_id=product_pk)
# #         return Review.objects.none()

# #     def get_serializer_context(self):
# #         return {'product_id': self.kwargs.get('product_pk')}  

# class ReviewViewSet(ModelViewSet):
#      # queryset = Review.objects.all()
#      serializer_class = ReviewSerializer
     
#      def get_queryset(self):
#           # if getattr(self, 'swagger_fake_view', False):  
#           #      return Review.objects.none()
#           return Review.objects.filter(product_id=self.kwargs.get('product_pk'))
#      def get_serializer_context(self):
#           return {'product_id':self.kwargs.get('product_pk')}
# # @api_view(['GET','POST'])
# # def view_products(request):
# #      if request.method == "GET":
# #         products = Product.objects.select_related('category').all()
# #         serializer = ProductSerializer(products,many= True)
# #         return Response(serializer.data)
# #      if request.method =='POST':
# #           serializer = ProductSerializer(data = request.data)
# #           serializer.is_valid(raise_exception=True)
# #           print(serializer.validated_data)
# #           serializer.save()
# #           return Response(serializer.data, status=status.HTTP_201_CREATED)
        
# #           # if serializer.is_valid():
# #           #      print(serializer.validated_data)
# #           #      serializer.save()
# #           #      return Response(serializer.data, status=status.HTTP_201_CREATED)
# #           # else:
# #           #      return Response(serializer, status=status.HTTP_400_BAD_REQUEST)
# # class ViewProducts(APIView):
# #      def get(self,request):
# #           products = Product.objects.select_related('category').all()
# #           serializer = ProductSerializer(products,many=True)
# #           return Response(serializer.data,)
# #      def post(self,request):
# #           serializer = ProductSerializer(data = request.data)
# #           serializer.is_valid(raise_exception=True)
# #           serializer.save()
# #           return Response(serializer.data,status=status.HTTP_201_CREATED)

# # class ViewSpecificProduct(APIView):
# #     def get(self,request,id):
# #          product = get_object_or_404(Product,pk=id)
# #          serializer =  ProductSerializer(product)
# #          return Response(serializer.data)
# #     def put(self,request,id):
# #          product = get_object_or_404(Product,pk= id)
# #          serializer = ProductSerializer(product,data = request.data)
# #          serializer.is_valid(raise_exception = True)
# #          serializer.save()
# #          return Response(serializer.data)
# #     def delete(self,request,id):
# #          product = get_object_or_404(Product,pk=id)
# #          copy_of_product =  product
# #          product.delete()

# #          serializer = ProductSerializer(copy_of_product)
# #          return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
# # class ProductList(ListCreateAPIView):
# #      queryset = Product.objects.select_related('category').all()
# #      serializer_class = ProductSerializer
# #      # def get_queryset(self):
# #      #      return Product.objects.select_related('category').all()
# #      # def get_serializer_class(self):
# #      #      return ProductSerializer
# #      # def get_serializer_context(self):
# #      #      return {'request':self.request}
# # @api_view(['GET','PUT','DELETE'])
# # def view_specific_product(request,id):
# #       if request.method == 'GET':
# #           product = get_object_or_404(Product,pk=id)
# #           serializer = ProductSerializer(product)
# #     #   product_dict  = {'id':product.id,'name':product.name,'price':product.price}
# #           return Response(serializer.data)
# #       if request.method == "PUT":
# #            product = get_object_or_404(Product,pk=id)
# #            serializer = ProductSerializer(product,data=request.data)
# #            serializer.is_valid(raise_exception=True)
# #            serializer.save()
# #            return Response(serializer.data)
# #       if request.Method == "DELETE":
# #            product= get_object_or_404(Product, pk=id)
# #            copy_of_product = product

# #            product.delete()
# #            serializer = ProductSerializer (copy_of_product)
# #            return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)    

# #     # try:
# #     #     product = Product.objects.get(pk=id)
# #     #     product_dict  = {'id':product.id,'name':product.name,'price':product.price}
# #     #     return Response(product_dict)
# #     # except Product.DoesNotExist:

# #     #     return Response({"message":"Product does not exists"},status = status.HTTP_404_NOT_FOUND)
# # class ViewCategories(APIView):
# #      def get(self,request):
# #           categories = Category.objects.annotate(product_count = Count('products')).all()
# #           serializer = CategorySerializer(categories,many=True)
# #           return Response(serializer.data)
# #      def post(self, request):
# #           serializer = CategorySerializer(data = request.data)
# #           serializer.is_valid(raise_exception=True)
# #           serializer.save()
# #           return Response(serializer.data, status=status.HTTP_201_CREATED) 
     
# # class CategoryList(ListCreateAPIView):
# #      def get_queryset(self):
# #           return Category.objects.annotate(product_count = Count('products')).all()
# #      def get_serializer_class(self):
# #           return CategorySerializer
     


# # @api_view(['GET','POST'])
# # def view_categories(request):
# #     if request.method =='GET':
# #           categories =  Category.objects.annotate(product_count = Count('products')).all()
# #           serializer = CategorySerializer(categories, many= True)
# #           return Response(serializer.data)
# #     if request.method == "POST":
# #          serializer = CategorySerializer(data=request.data)
# #          if serializer.is_valid():
# #               serializer.save()
# #               return  Response(serializer.data,status=status.HTTP_201_CREATED)
# #          else:
# #               return Response(serializer,status=status.HTTP_400_BAD_REQUEST)
         
# # class ViewSpecificCategory(APIView):
# #      def get (self,request,id):
# #           category = get_object_or_404(
# #                Category.objects.annotate(product_count = Count('products')),pk=id)
# #           serializer = CategorySerializer(category)
# #           return Response(serializer.data)
     
# #      def put(self,request,id):
# #           category = get_object_or_404(Category.objects.annotate(product_count = Count('products')),pk=id)
# #           serializer = CategorySerializer(category,data = request.data)
# #           serializer.is_valid(raise_exception=True)
# #           serializer.save()
# #           return Response(serializer.data)
# #      def delete(self,request,id):
# #           category = get_object_or_404(Category.objects.annotate(product_count = Count('products')),pk=id)
# #           category.delete()
# #           return Response(status=status.HTTP_204_NO_CONTENT)

# # class CategoryDetails(RetrieveUpdateDestroyAPIView):
# #      queryset = Category.objects.annotate(product_count = Count('products')).all()
# #      serializer_class = CategorySerializer
# #      lookup_field = "id"
     

# # @api_view()
# # def view_specific_category(request,pk):
# #      category =  get_object_or_404(Category,pk=pk)
# #      serializer = CategorySerializer(category)
# #      return Response(serializer.data)


