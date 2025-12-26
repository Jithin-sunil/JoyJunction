from django.shortcuts import render,redirect
from Guest.models import *
from Seller.models import *
from User.models import *
from django.db.models import Sum
from django.http import JsonResponse
from datetime import datetime
# Create your views here.

def HomePage(request):
    return render(request,'User/Homepage.html')

def Myprofile(request):
    userdata = tbl_user.objects.get(id=request.session['uid'])
    return render(request,'User/Myprofile.html',{'userdata':userdata})

def EditProfile(request):
    userdata = tbl_user.objects.get(id=request.session['uid'])
    if request.method == "POST":
        userdata.user_name = request.POST.get("txt_name")
        userdata.user_email = request.POST.get("txt_email")
        userdata.user_contact = request.POST.get("txt_contact")
        userdata.user_address = request.POST.get("txt_address")
        if request.FILES.get("file_photo"):
            userdata.user_photo = request.FILES.get("file_photo")
        userdata.save()
        return render(request,'User/EditProfile.html',{'userdata':userdata,'msg':'Profile Updated Successfully'})
    else:
        return render(request,'User/EditProfile.html',{'userdata':userdata})

def ChangePassword(request):
    userdata = tbl_user.objects.get(id=request.session['uid'])
    if request.method == "POST":
        currentpassword = request.POST.get("txt_currentpassword")
        newpassword = request.POST.get("txt_newpassword")
        confirmpassword = request.POST.get("txt_confirmpassword")
        if userdata.user_password == currentpassword:
            if newpassword == confirmpassword:
                userdata.user_password = newpassword
                userdata.save()
                return render(request,'User/ChangePassword.html',{'msg':'Password Changed Successfully'})
            else:
                return render(request,'User/ChangePassword.html',{'error':'New Password and Confirm Password are not matching'})
        else:
            return render(request,'User/ChangePassword.html',{'error':'Current Password is Incorrect'})
    else:
        return render(request,'User/ChangePassword.html')

def ViewProduct(request):
    categorys = tbl_category.objects.all()
    ar = [1, 2, 3, 4, 5]

    # ---------- Base queryset ----------
    products = tbl_product.objects.all()

    # ---------- POST FILTERING ----------
    if request.method == "POST":
        name = request.POST.get("txt_search")
        category_id = request.POST.get("sel_category")
        subcatergory_id = request.POST.get("sel_subcategory")

        if category_id == "" and subcatergory_id == "" and name != "":
            products = tbl_product.objects.filter(product_name__icontains=name)

        elif name != "" and category_id != "" and subcatergory_id == "":
            products = tbl_product.objects.filter(
                product_name__icontains=name,
                subcategory__category=category_id
            )

        elif name != "" and subcatergory_id != "" and category_id != "":
            products = tbl_product.objects.filter(
                product_name__icontains=name,
                subcategory=subcatergory_id
            )

        elif subcatergory_id != "":
            products = tbl_product.objects.filter(subcategory=subcatergory_id)

        elif category_id != "":
            products = tbl_product.objects.filter(subcategory__category=category_id)

        else:
            products = tbl_product.objects.all()

    # ---------- COMMON LOGIC (USED FOR BOTH GET & POST) ----------
    parry = []

    for i in products:
        total_stock = tbl_stock.objects.filter(
            product=i.id
        ).aggregate(total=Sum('stock_quantity'))['total'] or 0

        total_cart = tbl_cart.objects.filter(
            product=i.id,
            cart_status=1
        ).aggregate(total=Sum('cart_quantity'))['total'] or 0

        i.total_stock = total_stock - total_cart

        tot = 0
        ratecount = tbl_rating.objects.filter(product=i.id).count()

        if ratecount > 0:
            ratedata = tbl_rating.objects.filter(product=i.id)
            for j in ratedata:
                tot += j.rating_data
            avg = tot // ratecount
            parry.append(avg)
        else:
            parry.append(0)

    datas = zip(products, parry)

    # ---------- SINGLE RENDER ----------
    return render(
        request,
        'User/ViewProduct.html',
        {
            'products': datas,
            'categorys': categorys,
            'ar': ar
        }
    )


def ViewMore(request, pid):
    product = tbl_product.objects.get(id=pid)
    gallery = tbl_gallery.objects.filter(product=product)

    total_stock = tbl_stock.objects.filter(
        product=product
    ).aggregate(total=Sum('stock_quantity'))['total'] or 0

    total_cart = tbl_cart.objects.filter(
        product=product,
        cart_status=1
    ).aggregate(total=Sum('cart_quantity'))['total'] or 0

    available = total_stock - total_cart

    ratecount = tbl_rating.objects.filter(product=product).count()
    avg = 0

    if ratecount > 0:
        tot = tbl_rating.objects.filter(product=product)\
            .aggregate(total=Sum('rating_data'))['total'] or 0
        avg = tot // ratecount

    seller = product.seller
    ar = [1, 2, 3, 4, 5]  

    return render(request, 'User/ViewMore.html', {
        'product': product,
        'gallery': gallery,
        'available': available,
        'avg': avg,
        'ratecount': ratecount,
        'seller': seller,
        'ar': ar
    })

def AddCart(request,pid):
    productdata=tbl_product.objects.get(id=pid)
    userdata=tbl_user.objects.get(id=request.session["uid"])
    bookingcount=tbl_booking.objects.filter(user=userdata,booking_status=0).count()
    if bookingcount>0:
        bookingdata=tbl_booking.objects.get(user=userdata,booking_status=0)
        cartcount=tbl_cart.objects.filter(booking=bookingdata,product=productdata).count()
        if cartcount>0:
            msg="Already added"
            return render(request,"User/ViewProduct.html",{'msg':msg})
        else:
            tbl_cart.objects.create(booking=bookingdata,product=productdata)
            msg="Added To cart"
            return render(request,"User/ViewProduct.html",{'msg':msg})
    else:
        bookingdata = tbl_booking.objects.create(user=userdata)
        tbl_cart.objects.create(booking=tbl_booking.objects.get(id=bookingdata.id),product=productdata)
        msg="Added To cart"
        return render(request,"User/ViewProduct.html",{'msg':msg})

def MyCart(request):
    if request.method=="POST":
        bookingdata=tbl_booking.objects.get(id=request.session["bookingid"])
        bookingdata.booking_amount=request.POST.get("carttotalamt")
        bookingdata.booking_status=1
        bookingdata.save()
        cart = tbl_cart.objects.filter(booking=bookingdata)
        for i in cart:
            i.cart_status = 1
            i.save()
        return redirect("User:Payment")
    else:
        bookcount = tbl_booking.objects.filter(user=request.session["uid"],booking_status=0).count()
        if bookcount > 0:
            book = tbl_booking.objects.get(user=request.session["uid"],booking_status=0)
            request.session["bookingid"] = book.id
            cart = tbl_cart.objects.filter(booking=book)
            for i in cart:
                total_stock = tbl_stock.objects.filter(product=i.product.id).aggregate(total=Sum('stock_quantity'))['total']
                total_cart = tbl_cart.objects.filter(product=i.product.id, cart_status=1).aggregate(total=Sum('cart_quantity'))['total']
                # print(total_stock)
                # print(total_cart)
                if total_stock is None:
                    total_stock = 0
                if total_cart is None:
                    total_cart = 0
                total =  total_stock - total_cart
                i.total_stock = total
            return render(request,"User/MyCart.html",{'cartdata':cart})
        else:
            return render(request,"User/MyCart.html")
   
def DelCart(request,did):
   tbl_cart.objects.get(id=did).delete()
   return redirect("User:MyCart")

def CartQty(request):
   qty=request.GET.get('QTY')
   cartid=request.GET.get('ALT')
   cartdata=tbl_cart.objects.get(id=cartid)
   cartdata.cart_quantity=qty
   cartdata.save()
   return redirect("User:MyCart")

def Payment(request):
    bookingdata = tbl_booking.objects.get(id=request.session["bookingid"])
    amount = bookingdata.booking_amount

    if request.method == "POST":
        bookingdata.booking_status = 2
        bookingdata.save()

        cart = tbl_cart.objects.filter(booking=bookingdata)
        for i in cart:
            i.cart_status = 2
            i.save()

        return redirect("User:Loader")
    else:
            return render(request,"User/Payment.html",{'amount':amount})

def Loader(request):
    return render(request,"User/Loader.html")

def Payment_suc(request):
    return render(request,"User/Payment_suc.html")

def MyBooking(request):
    bookingdata = tbl_booking.objects.filter(user=request.session['uid'],booking_status__gte=0)
    return render(request,"User/MyBooking.html",{'bookingdata':bookingdata})

def rating(request,mid):
    parray=[1,2,3,4,5]
    mid=mid
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
        return render(request,"User/Rating.html",{'mid':mid,'data':stardata,'ar':parray,'avg':avg,'count':counts})
    else:
         return render(request,"User/Rating.html",{'mid':mid})

def ajaxstar(request):
    parray=[1,2,3,4,5]
    rating_data=request.GET.get('rating_data')
    
    user_review=request.GET.get('user_review')
    pid=request.GET.get('pid')
    # wdata=tbl_booking.objects.get(id=pid)
    tbl_rating.objects.create(user=tbl_user.objects.get(id=request.session['uid']),user_review=user_review,rating_data=rating_data,product=tbl_product.objects.get(id=pid))
    stardata=tbl_rating.objects.filter(product=pid).order_by('-datetime')
    return render(request,"User/AjaxRating.html",{'data':stardata,'ar':parray})

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


def Complaint(request):
    complaintdata = tbl_complaint.objects.filter(user=request.session['uid'])
    if request.method == "POST":
        title = request.POST.get("txt_title")
        content = request.POST.get("txt_content")
        userdata = tbl_user.objects.get(id=request.session['uid'])
        tbl_complaint.objects.create(user=userdata,complaint_title=title,complaint_content=content)
        return render(request,'User/Complaint.html',{'msg':'Complaint Submitted Successfully'})
    else:
        return render(request,'User/Complaint.html',{'complaintdata':complaintdata})
    
def DeleteComplaint(request,cid):
    tbl_complaint.objects.get(id=cid).delete()
    return redirect("User:Complaint")