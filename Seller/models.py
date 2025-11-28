from django.db import models
from Admin.models import *
from Guest.models import *
# Create your models here.

class tbl_product(models.Model):
    product_name = models.CharField(max_length=100)
    product_description = models.CharField(max_length=500)
    product_price = models.IntegerField()
    product_photo = models.FileField(upload_to='Assets/ProductPhotos/')
    seller = models.ForeignKey(tbl_seller, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(tbl_subcategory, on_delete=models.CASCADE)

class tbl_stock(models.Model):
    stock_quantity = models.IntegerField()
    stock_date = models.DateField(auto_now_add=True)
    product = models.ForeignKey(tbl_product, on_delete=models.CASCADE)

class tbl_gallery(models.Model):
    gallery_photo = models.FileField(upload_to='Assets/ProductPhotos/')
    product = models.ForeignKey(tbl_product, on_delete=models.CASCADE)