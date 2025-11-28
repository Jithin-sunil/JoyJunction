from django.shortcuts import render
from Guest.models import *
# Create your views here.

def Homepage(request):
    return render(request,'User/Homepage.html')

def Myprofile(request):
    userid = request.session['userid']
    userdata = tbl_user.objects.get(id=userid)
    return render(request,'User/Myprofile.html',{'userdata':userdata})

def EditProfile(request):
    userid = request.session['userid']
    userdata = tbl_user.objects.get(id=userid)
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
    userid = request.session['userid']
    userdata = tbl_user.objects.get(id=userid)
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
                return render(request,'User/ChangePassword.html',{'msg':'New Password and Confirm Password are not matching'})
        else:
            return render(request,'User/ChangePassword.html',{'msg':'Current Password is Incorrect'})
    else:
        return render(request,'User/ChangePassword.html')