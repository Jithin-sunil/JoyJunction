from django.shortcuts import render,redirect
from Admin.models import *
from Guest.models import *
from User.models import *
# Create your views here.

def Homepage(request):
    return render(request,'Admin/Homepage.html')

def AdminRegistration(request):
    admindata=tbl_admin.objects.all()
    if request.method=='POST':
        name=request.POST.get('txt_name')
        email=request.POST.get('txt_email')
        password=request.POST.get('txt_password')
        tbl_admin.objects.create(
            admin_name=name,
            admin_email=email,
            admin_password=password
        )
        return render(request,'Admin/AdminRegistration.html',{'msg':"Admin Registered Successfully"})
    else:
        return render(request,'Admin/AdminRegistration.html',{'admindata':admindata})

def deladmin(request,did):
    tbl_admin.objects.get(id=did).delete()
    return redirect('Admin:AdminRegistration')

def editadmin(request,eid):
    adminobj=tbl_admin.objects.get(id=eid)
    admindata=tbl_admin.objects.all()
    if request.method=='POST':
        adminobj.admin_name=request.POST.get('txt_name')
        adminobj.admin_email=request.POST.get('txt_email')
        adminobj.admin_password=request.POST.get('txt_password')
        adminobj.save()
        return render(request,'Admin/AdminRegistration.html',{'msg':"Admin Data Updated Successfully"})
    else:
        return render(request,'Admin/AdminRegistration.html',{'adminobj':adminobj,'admindata':admindata})

def District(request):
    districtdata=tbl_district.objects.all()
    if request.method=='POST':
        districtname=request.POST.get('txt_district')
        tbl_district.objects.create(
            district_name=districtname
        )
        return render(request,'Admin/District.html',{'msg':"District Added Successfully"})
    else:
        return render(request,'Admin/District.html',{'districtdata':districtdata})

def deldistrict(request,did):
    tbl_district.objects.get(id=did).delete()
    return redirect('Admin:District')

def editdistrict(request,eid):
    districtobj=tbl_district.objects.get(id=eid)
    if request.method=='POST':
        districtobj.district_name=request.POST.get('txt_district')
        districtobj.save()
        return render(request,'Admin/District.html',{'msg':"District Updated Successfully"})

    else:
        return render(request,'Admin/District.html',{'districtobj':districtobj})

def Place(request): 
    placedata=tbl_place.objects.all()
    districtdata=tbl_district.objects.all()
    if request.method=='POST':
        placename=request.POST.get('txt_place')
        districtobj=tbl_district.objects.get(id=request.POST.get('sel_district'))
        tbl_place.objects.create(
            place_name=placename,
            district=districtobj
        )
        return render(request,'Admin/Place.html',{'msg':"Place Added Successfully"})
    else:
        return render(request,'Admin/Place.html',{'placedata':placedata,'districtdata':districtdata})

def delplace(request,did):
    tbl_place.objects.get(id=did).delete()
    return redirect('Admin:Place')

def editplace(request,eid):
    placeobj=tbl_place.objects.get(id=eid)
    districtdata=tbl_district.objects.all()
    if request.method=='POST':
        placeobj.place_name=request.POST.get('txt_place')
        districtobj=tbl_district.objects.get(id=request.POST.get('sel_district'))
        placeobj.district_id=districtobj
        placeobj.save()
        return render(request,'Admin/Place.html',{'msg':"Place Updated Successfully"})

    else:
        return render(request,'Admin/Place.html',{'placeobj':placeobj,'districtdata':districtdata})

def Category(request):
    categorydata=tbl_category.objects.all()
    if request.method=='POST':
        categoryname=request.POST.get('txt_category')
        tbl_category.objects.create(
            category_name=categoryname
        )
        return render(request,'Admin/Category.html',{'msg':"Category Added Successfully"})
    else:
        return render(request,'Admin/Category.html',{'categorydata':categorydata})

def delcategory(request,did):
    tbl_category.objects.get(id=did).delete()
    return redirect('Admin:Category')

def editcategory(request,eid):
    categoryobj=tbl_category.objects.get(id=eid)
    if request.method=='POST':
        categoryobj.category_name=request.POST.get('txt_category')
        categoryobj.save()
        return render(request,'Admin/Category.html',{'msg':"Category Updated Successfully"})

    else:
        return render(request,'Admin/Category.html',{'categoryobj':categoryobj})

def SubCategory(request):
    subcategorydata=tbl_subcategory.objects.all()
    categorydata=tbl_category.objects.all()
    if request.method=='POST':
        subcategoryname=request.POST.get('txt_subcategory')
        categoryobj=tbl_category.objects.get(id=request.POST.get('sel_category'))
        tbl_subcategory.objects.create(
            subcategory_name=subcategoryname,
            category=categoryobj
        )
        return render(request,'Admin/SubCategory.html',{'msg':"SubCategory Added Successfully"})
    else:
        return render(request,'Admin/SubCategory.html',{'subcategorydata':subcategorydata,'categorydata':categorydata})

    
def delsubcategory(request,did):
    tbl_subcategory.objects.get(id=did).delete()
    return redirect('Admin:SubCategory')

def editsubcategory(request,eid):
    subcategoryobj=tbl_subcategory.objects.get(id=eid)
    categorydata=tbl_category.objects.all()
    if request.method=='POST':
        subcategoryobj.subcategory_name=request.POST.get('txt_subcategory')
        categoryobj=tbl_category.objects.get(id=request.POST.get('sel_category'))
        subcategoryobj.category_id=categoryobj
        subcategoryobj.save()
        return render(request,'Admin/SubCategory.html',{'msg':"SubCategory Updated Successfully"})

    else:
        return render(request,'Admin/SubCategory.html',{'subcategoryobj':subcategoryobj,'categorydata':categorydata})

def SellerVerification(request):
    sellerdata=tbl_seller.objects.filter(seller_status=0)
    verified = tbl_seller.objects.filter(seller_status=1)
    rejected = tbl_seller.objects.filter(seller_status=2)
    return render(request,'Admin/SellerVerification.html',{'sellerdata':sellerdata,'verified':verified,'rejected':rejected})

def verifyseller(request,vid):
    sellerobj=tbl_seller.objects.get(id=vid)
    sellerobj.seller_status=1
    sellerobj.save()
    return redirect('Admin:SellerVerification')

def rejectseller(request,rid):
    sellerobj=tbl_seller.objects.get(id=rid)
    sellerobj.seller_status=2
    sellerobj.save()
    return redirect('Admin:SellerVerification')


def UserList(request):
    userdata=tbl_user.objects.all()
    return render(request,'Admin/UserList.html',{'userdata':userdata})

def ViewComplaint(request):
    complaintdata=tbl_complaint.objects.all()
    return render(request,'Admin/ViewComplaint.html',{'complaintdata':complaintdata})

def ReplyComplaint(request,cid):
    complaintobj=tbl_complaint.objects.get(id=cid)
    if request.method=='POST':
        reply=request.POST.get('txt_reply')
        complaintobj.complaint_reply=reply
        complaintobj.complaint_status=1
        complaintobj.save()
        return redirect('Admin:ViewComplaint')
    else:
        return render(request,'Admin/Reply.html',{'complaintobj':complaintobj})