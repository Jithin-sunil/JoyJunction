from django.urls import path
from User import views
app_name = 'User'
urlpatterns = [
    path('HomePage/', views.HomePage, name='HomePage'),
    path('Myprofile/', views.Myprofile, name='Myprofile'),
    path('EditProfile/', views.EditProfile, name='EditProfile'),
    path('ChangePassword/', views.ChangePassword, name='ChangePassword'),
    path('ViewProduct/', views.ViewProduct, name='ViewProduct'),
    path('AddCart/<int:pid>/', views.AddCart, name='AddCart'),
    path('MyCart/', views.MyCart, name='MyCart'),
    path('DelCart/<int:did>/', views.DelCart, name='DelCart'),
    path('CartQty/', views.CartQty, name='CartQty'),
    path('Payment/', views.Payment, name='Payment'),
    path('Loader/', views.Loader, name='Loader'),
    path('Payment_suc/', views.Payment_suc, name='Payment_suc'),
    path('MyBooking/',views.MyBooking,name="MyBooking"),
    path('rating/<int:mid>',views.rating,name="rating"),  
    path('ajaxstar/',views.ajaxstar,name="ajaxstar"),
    path('starrating/',views.starrating,name="starrating"),
    path('Complaint/', views.Complaint, name='Complaint'),
    path('DeleteComplaint/<int:cid>/', views.DeleteComplaint, name='DeleteComplaint'),
]