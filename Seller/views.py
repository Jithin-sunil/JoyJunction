from django.shortcuts import render,redirect
from Seller.models import *
from User.models import *
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
        return render(request, 'Seller/Stock.html', { 'msg': 'Stock Added Successfully','pid':pid})
    else:
        return render(request, 'Seller/Stock.html', { 'stockdata': stock,'pid':pid})

def delstock(request, sid, pid):
    tbl_stock.objects.get(id=sid).delete()
    return redirect('Seller:AddStock', pid=pid)

def Gallery(request, pid):
    galleryphotos = tbl_gallery.objects.filter(product=pid)
    if request.method == "POST":
        photos = request.FILES.getlist("file_photo")
        product = tbl_product.objects.get(id=pid)
        for photo in photos:
            tbl_gallery.objects.create(
                gallery_photo=photo,
                product=product
            )
        return render(request, 'Seller/Gallery.html', {'msg': 'Photos Added Successfully','pid':pid})
    else:
        return render(request, 'Seller/Gallery.html', {'galleryphotos': galleryphotos,'pid':pid})

def delgallery(request, gid, pid):
    tbl_gallery.objects.get(id=gid).delete()
    return redirect('Seller:Gallery', pid=pid)

def ViewBookings(request):
    bookings = tbl_booking.objects.filter(tbl_cart__product__seller_id=request.session['sid'])
    return render(request, 'Seller/ViewBookings.html', {'bookings': bookings})

def UpdateCartStatus(request, cid, status):
    cart = tbl_cart.objects.get(id=cid)
    cart.cart_status = status
    cart.save()
    booking = cart.booking
    total_items = tbl_cart.objects.filter(booking=booking).count()
    delivered_items = tbl_cart.objects.filter(booking=booking,cart_status=6).count()
    if total_items == delivered_items:
        booking.booking_status = 3
        booking.save()
    return redirect("Seller:ViewBookings")


def ViewRating(request,pid):
    parray=[1,2,3,4,5]
    mid=pid
    # wdata=tbl_booking.objects.get(id=mid)
    
    counts=0
    counts=stardata=tbl_rating.objects.filter(product=mid).count()
    if counts>0:
        res=0
        stardata=tbl_rating.objects.filter(product=mid).order_by('-datetime')
        for i in stardata:
            res=res+i.rating_data
        avg=res//counts
        # print(avg)
        return render(request,"Seller/ViewRating.html",{'mid':mid,'data':stardata,'ar':parray,'avg':avg,'count':counts})
    else:
         return render(request,"Seller/ViewRating.html",{'mid':mid})

def starrating(request):
    r_len = 0
    five = four = three = two = one = 0
    # cdata = tbl_booking.objects.get(id=request.GET.get("pdt"))
    rate = tbl_rating.objects.filter(product=request.GET.get("pdt"))
    ratecount = tbl_rating.objects.filter(product=request.GET.get("pdt")).count()
    for i in rate:
        if int(i.rating_data) == 5:
            five = five + 1
        elif int(i.rating_data) == 4:
            four = four + 1
        elif int(i.rating_data) == 3:
            three = three + 1
        elif int(i.rating_data) == 2:
            two = two + 1
        elif int(i.rating_data) == 1:
            one = one + 1
        else:
            five = four = three = two = one = 0
        # print(i.rating_data)
        # r_len = r_len + int(i.rating_data)
    # rlen = r_len // 5
    # print(rlen)
    result = {"five":five,"four":four,"three":three,"two":two,"one":one,"total_review":ratecount}
    return JsonResponse(result)