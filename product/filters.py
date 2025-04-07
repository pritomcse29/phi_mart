from django_filters.rest_framework import FilterSet
from product.models import Product
import django_filters


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields ={
            'category_id':['exact'],
            'price':['gt','lt']
        }