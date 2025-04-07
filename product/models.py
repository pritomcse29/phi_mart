from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator,MaxValueValidator,FileExtensionValidator
from product.validators import validate_file_size
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null =True)

    def __str__(self):
        return self.name
class Product(models.Model):
    name = models.CharField(max_length=200)
    description =  models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.PositiveIntegerField()
 
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
         ordering = ['-id',]
    def __str__(self):
        return self.name
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="products/images/", validators=[validate_file_size])
    # file = models.FileField(upload_to="product/files",validators=FileExtensionValidator(['pdf']))


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name =  models.CharField(max_length=255)
    description =  models.TextField()
    date =  models.DateField(auto_now_add=True)
