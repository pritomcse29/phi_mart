from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from product.models import Product,Category
from rest_framework import status
from django.shortcuts import get_object_or_404
from product.serializers import ProductSerializer,CategorySerializer
from django.db.models import Count
from rest_framework.views import APIView

# Create your views here.
@api_view(['GET','POST'])
def view_products(request):
     if request.method == "GET":
        products = Product.objects.select_related('category').all()
        serializer = ProductSerializer(products,many= True)
        return Response(serializer.data)
     if request.method =='POST':
          serializer = ProductSerializer(data = request.data)
          serializer.is_valid(raise_exception=True)
          print(serializer.validated_data)
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
        
          # if serializer.is_valid():
          #      print(serializer.validated_data)
          #      serializer.save()
          #      return Response(serializer.data, status=status.HTTP_201_CREATED)
          # else:
          #      return Response(serializer, status=status.HTTP_400_BAD_REQUEST)
class ViewProducts(APIView):
     def get(self,request):
          products = Product.objects.select_related('category').all()
          serializer = ProductSerializer(products,many=True)
          return Response(serializer.data,)
     def post(self,request):
          serializer = ProductSerializer(data = request.data)
          serializer.is_valid(raise_exception=True)
          serializer.save()
          return Response(serializer.data,status=status.HTTP_201_CREATED)

class ViewSpecificProduct(APIView):
    def get(self,request,id):
         product = get_object_or_404(Product,pk=id)
         serializer =  ProductSerializer(product)
         return Response(serializer.data)
    def put(self,request,id):
         product = get_object_or_404(Product,pk= id)
         serializer = ProductSerializer(product,data = request.data)
         serializer.is_valid(raise_exception = True)
         serializer.save()
         return Response(serializer.data)
    def delete(self,request,id):
         product = get_object_or_404(Product,pk=id)
         copy_of_product =  product
         product.delete()

         serializer = ProductSerializer(copy_of_product)
         return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
@api_view(['GET','PUT','DELETE'])
def view_specific_product(request,id):
      if request.method == 'GET':
          product = get_object_or_404(Product,pk=id)
          serializer = ProductSerializer(product)
    #   product_dict  = {'id':product.id,'name':product.name,'price':product.price}
          return Response(serializer.data)
      if request.method == "PUT":
           product = get_object_or_404(Product,pk=id)
           serializer = ProductSerializer(product,data=request.data)
           serializer.is_valid(raise_exception=True)
           serializer.save()
           return Response(serializer.data)
      if request.Method == "DELETE":
           product= get_object_or_404(Product, pk=id)
           copy_of_product = product

           product.delete()
           serializer = ProductSerializer (copy_of_product)
           return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)    

    # try:
    #     product = Product.objects.get(pk=id)
    #     product_dict  = {'id':product.id,'name':product.name,'price':product.price}
    #     return Response(product_dict)
    # except Product.DoesNotExist:

    #     return Response({"message":"Product does not exists"},status = status.HTTP_404_NOT_FOUND)
class ViewCategories(APIView):
     def get(self,request):
          categories = Category.objects.annotate(product_count = Count('products')).all()
          serializer = CategorySerializer(categories,many=True)
          return Response(serializer.data)
     def post(self, request):
          serializer = CategorySerializer(data = request.data)
          serializer.is_valid(raise_exception=True)
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED) 

@api_view(['GET','POST'])
def view_categories(request):
    if request.method =='GET':
          categories =  Category.objects.annotate(product_count = Count('products')).all()
          serializer = CategorySerializer(categories, many= True)
          return Response(serializer.data)
    if request.method == "POST":
         serializer = CategorySerializer(data=request.data)
         if serializer.is_valid():
              serializer.save()
              return  Response(serializer.data,status=status.HTTP_201_CREATED)
         else:
              return Response(serializer,status=status.HTTP_400_BAD_REQUEST)
         
class ViewSpecificCategory(APIView):
     def get (self,request,id):
          category = get_object_or_404(
               Category.objects.annotate(product_count = Count('products')),pk=id)
          serializer = CategorySerializer(category)
          return Response(serializer.data)
     
     def put(self,request,id):
          category = get_object_or_404(Category.objects.annotate(product_count = Count('products')),pk=id)
          serializer = CategorySerializer(category,data = request.data)
          serializer.is_valid(raise_exception=True)
          serializer.save()
          return Response(serializer.data)
     def delete(self,request,id):
          category = get_object_or_404(Category.objects.annotate(product_count = Count('products')),pk=id)
          category.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def view_specific_category(request,pk):
     category =  get_object_or_404(Category,pk=pk)
     serializer = CategorySerializer(category)
     return Response(serializer.data)