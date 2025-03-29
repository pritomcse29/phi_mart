from rest_framework import serializers
from decimal import Decimal
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
   class Meta:
        model = Category
        fields = ['id','name','description','product_count']
   product_count = serializers.IntegerField(read_only=True)
#    product_count = serializers.SerializerMethodField(method_name='get_product_count')

#    def get_product_count(self, category):

#         count = Product.objects.filter(category=category).count()
#         return count
    # id = serializers.IntegerField()
    # name = serializers.CharField()
    # description = serializers.CharField()


# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField()
#     unit_price = serializers.DecimalField(max_digits=10,decimal_places=2,source='price')



#     price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
     
#     # category = serializers.PrimaryKeyRelatedField(
#     #     
#     # )
#     # category = serializers.StringRelatedField()

#     # category = CategorySerializer()
#     category = serializers.HyperlinkedRelatedField(
#         queryset = Category.objects.all(),
#         view_name = 'view_specific_category'
#     )

#     def calculate_tax(self,product):
#         return round(product.price * Decimal(1.1),2)
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Product
        # "__all__"
        fields = ['id','name','description','price','stock','category','price_with_tax']

    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # category = serializers.HyperlinkedRelatedField(
    #     queryset = Category.objects.all(),
    #     view_name = 'view_specific_category'
    # )
   
    def calculate_tax(self,product):
           return round(product.price * Decimal(1.1),2)
    def validate_price(self,price):
         if price < 0:
              raise serializers.ValidationError('Only greater than 0 value is accepted')
         return price