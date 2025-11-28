from django.shortcuts import render,redirect
from Guest.models import *
from Admin.models import *
# Create your views here.


def UserRegistration(request):
    districtdata = tbl_district.objects.all()
    if request.method == "POST":
        name =request.POST.get("txt_name")
        email =request.POST.get("txt_email")
        contact =request.POST.get("txt_contact")
        address =request.POST.get("txt_address")
        photo =request.FILES.get("file_photo")
        password =request.POST.get("txt_password")
        placeid =tbl_place.objects.get(id=request.POST.get("sel_place"))
        tbl_user.objects.create(
            user_name=name,
            user_email=email,
            user_contact=contact,
            user_address=address,
            user_photo=photo,
            user_password=password,
            place=placeid,
        )
        return render(request,'Guest/UserRegistration.html',{'msg':'Registration Successful'})
    else:
        return render(request,'Guest/UserRegistration.html',{'districtdata':districtdata})

def AjaxPlace(request):
    districtid = request.GET.get('did')
    placedata = tbl_place.objects.filter(district=districtid)
    return render(request,'Guest/AjaxPlace.html',{'placedata':placedata})

def SellerRegistration(request):
    districtdata = tbl_district.objects.all()
    if request.method == "POST":
        name =request.POST.get("txt_name")
        email =request.POST.get("txt_email")
        contact =request.POST.get("txt_contact")
        address =request.POST.get("txt_address")
        photo =request.FILES.get("file_photo")
        proof =request.FILES.get("file_proof")
        password =request.POST.get("txt_password")
        placeid =tbl_place.objects.get(id=request.POST.get("sel_place"))
        tbl_seller.objects.create(
            seller_name=name,
            seller_email=email,
            seller_contact=contact,
            seller_address=address,
            seller_photo=photo,
            seler_proof=proof,
            seller_password=password,
            place=placeid,
        )
        return render(request,'Guest/SellerRegistration.html',{'msg':'Registration Successful'})
    else:
        return render(request,'Guest/SellerRegistration.html',{'districtdata':districtdata})


def Login(request):
    if request.method == "POST":
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")
        
        usercount = tbl_user.objects.filter(user_email=email,user_password=password).count()
        admincount = tbl_admin.objects.filter(admin_email=email,admin_password=password).count()
        sellercount = tbl_seller.objects.filter(seller_email=email,seller_password=password).count()
        if usercount >0:
            userdata = tbl_user.objects.get(user_email=email,user_password=password)
            request.session['user_id'] = userdata.id
            return redirect('User:HomePage')
        elif admincount >0:
            admindata = tbl_admin.objects.get(admin_email=email,admin_password=password)
            request.session['admin_id'] = admindata.id
            return redirect('Admin:HomePage')
        elif sellercount >0:
            sellerdata = tbl_seller.objects.get(seller_email=email,seller_password=password)
            if sellerdata.seller_status == 1:
                request.session['seller_id'] = sellerdata.id
                return redirect('Seller:HomePage')
            elif sellerdata.seller_status == 0:
                return render(request,'Guest/Login.html',{'msg':'Your account is pending approval'})
            else:
                return render(request,'Guest/Login.html',{'msg':'Your account is rejected, contact admin'})
        else:
            return render(request,'Guest/Login.html',{'msg':'Invalid Email or Password'})
    else:
        return render(request,'Guest/Login.html')
    