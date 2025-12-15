from django.db import models
from Admin.models import *

# Create your models here.

class tbl_user(models.Model):
    user_name = models.CharField(max_length=100)
    user_email = models.CharField(max_length=100)
    user_contact = models.CharField(max_length=15)
    user_address = models.CharField(max_length=200)
    user_photo = models.FileField(upload_to='Assets/UserDocs/')
    user_password = models.CharField(max_length=100)
    place = models.ForeignKey(tbl_place, on_delete=models.CASCADE)

class tbl_seller(models.Model):
    seller_name = models.CharField(max_length=100)
    seller_email = models.CharField(max_length=100)
    seller_contact = models.CharField(max_length=15)
    seller_address = models.CharField(max_length=200)
    seller_photo = models.FileField(upload_to='Assets/SellerDocs/')
    seller_proof = models.FileField(upload_to='Assets/SellerDocs/')
    seller_password = models.CharField(max_length=100)
    seller_status = models.IntegerField(default=0)
    seller_doj=models.DateField(auto_now_add=True)
    place = models.ForeignKey(tbl_place, on_delete=models.CASCADE)