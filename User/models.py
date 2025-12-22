from django.db import models
from Guest.models import *
from Seller.models import *


# Create your models here.

class tbl_booking(models.Model):
    booking_date = models.DateField(auto_now_add=True)
    booking_status = models.IntegerField(default=0)
    booking_amount = models.CharField(null=True)
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)

class tbl_cart(models.Model):
    cart_quantity = models.IntegerField(default=1)
    cart_status = models.IntegerField(default=0)
    booking = models.ForeignKey(tbl_booking, on_delete=models.CASCADE)
    product = models.ForeignKey(tbl_product, on_delete=models.CASCADE)

class tbl_rating(models.Model):
    rating_data=models.IntegerField()
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE)
    user_review=models.CharField(max_length=500)
    product=models.ForeignKey(tbl_product,on_delete=models.CASCADE)
    datetime=models.DateTimeField(auto_now_add=True)

class tbl_complaint(models.Model):
    complaint_title = models.CharField(max_length=200)
    complaint_content = models.CharField(max_length=1000)
    complaint_date = models.DateField(auto_now_add=True)
    complaint_status = models.IntegerField(default=0)
    complaint_reply = models.CharField(max_length=1000, null=True)
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)