from django.shortcuts import render
from Seller.models import *
# Create your views here.


def HomePage(request):
    return render(request,'Seller/Homepage.html')

def Myprofile(request):
    sellerdata = tbl_seller.objects.get(id=request.session['sid'])
    return render(request,'Seller/Myprofile.html',{'sellerdata':sellerdata})

def EditProfile(request):
    sellerdata = tbl_seller.objects.get(id=request.session['sid'])
    if request.method == "POST":
        sellerdata.seller_name = request.POST.get("txt_name")
        sellerdata.seller_email = request.POST.get("txt_email")
        sellerdata.seller_contact = request.POST.get("txt_contact")
        sellerdata.seller_address = request.POST.get("txt_address")
        if request.FILES.get("file_photo"):
            sellerdata.seller_photo = request.FILES.get("file_photo")
        sellerdata.save()
        return render(request,'Seller/EditProfile.html',{'sellerdata':sellerdata,'msg':'Profile Updated Successfully'})
    else:
        return render(request,'Seller/EditProfile.html',{'sellerdata':sellerdata})

def ChangePassword(request):
    sellerdata = tbl_seller.objects.get(id=request.session['sid'])
    if request.method == "POST":
        currentpassword = request.POST.get("txt_currentpassword")
        newpassword = request.POST.get("txt_newpassword")
        confirmpassword = request.POST.get("txt_confirmpassword")
        if sellerdata.seller_password == currentpassword:
            if newpassword == confirmpassword:
                sellerdata.seller_password = newpassword
                sellerdata.save()
                return render(request,'Seller/ChangePassword.html',{'msg':'Password Changed Successfully'})
            else:
                return render(request,'Seller/ChangePassword.html',{'error':'New Password and Confirm Password are not matching'})
        else:
            return render(request,'Seller/ChangePassword.html',{'error':'Current Password is Incorrect'})
    else:
        return render(request,'Seller/ChangePassword.html')

def AddProduct(request):
    categories = tbl_category.objects.all()
    products = tbl_product.objects.filter(seller=request.session['sid'])
    if request.method == "POST":
        product_name = request.POST.get("txt_name")
        subcategory_id = request.POST.get("sel_subcategory")
        price = request.POST.get("txt_price")
        description = request.POST.get("txt_description")
        product_image = request.FILES.get("file_photo")
        subcategory = tbl_subcategory.objects.get(id=subcategory_id)
        seller = tbl_seller.objects.get(id=request.session['sid'])
        tbl_product.objects.create(
            product_name=product_name,
            subcategory=subcategory,
            product_price=price,
            product_description=description,
            product_photo=product_image,
            seller=seller
        )
        return render(request, 'Seller/Product.html', {'categories': categories, 'msg': 'Product Added Successfully'})
    else:
        return render(request, 'Seller/Product.html', {'categories': categories, 'products': products})


def AjaxSubCategory(request):
    category_id = request.GET.get('cid')
    subcategories = tbl_subcategory.objects.filter(category=category_id)
    return render(request, 'Seller/AjaxSubCategory.html', {'subcategories': subcategories})

def delproduct(request, pid):
    product = tbl_product.objects.get(id=pid)
    product.delete()
    return render(request, 'Seller/Product.html', {'msg': 'Product Deleted Successfully'})


def AddStock(request, pid):
    stock = tbl_stock.objects.filter(product=pid)
    if request.method == "POST":
        quantity = request.POST.get("txt_quantity")
        product = tbl_product.objects.get(id=pid)
        tbl_stock.objects.create(
            stock_quantity=quantity,
            product=product
        )
        return render(request, 'Seller/Stock.html', { 'msg': 'Stock Added Successfully'})
    else:
        return render(request, 'Seller/Stock.html', { 'stockdata': stock})