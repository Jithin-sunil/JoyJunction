from django.urls import path
from Seller import views
app_name = 'Seller'
urlpatterns = [
    path('HomePage/', views.HomePage, name='HomePage'),
    path('Myprofile/', views.Myprofile, name='Myprofile'),
    path('EditProfile/', views.EditProfile, name='EditProfile'),
    path('ChangePassword/', views.ChangePassword, name='ChangePassword'),
    path('AddProduct/', views.AddProduct, name='AddProduct'),
    path('AjaxSubCategory/', views.AjaxSubCategory, name='AjaxSubCategory'),
    path('delproduct/<int:pid>/', views.delproduct, name='delproduct'),
    path('AddStock/<int:pid>/', views.AddStock, name='AddStock'),
]