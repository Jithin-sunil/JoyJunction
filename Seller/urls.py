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
    path('delstock/<int:sid>/<int:pid>/', views.delstock, name='delstock'),

    path('Gallery/<int:pid>/', views.Gallery, name='Gallery'),
    path('delgallery/<int:gid>/<int:pid>/', views.delgallery, name='delgallery'),

    path('ViewBookings/', views.ViewBookings, name='ViewBookings'),
    path('UpdateCartStatus/<int:cid>/<int:status>/',views.UpdateCartStatus,name='UpdateCartStatus'),

    path('ViewRating/<int:pid>/', views.ViewRating, name='ViewRating'),
    path('starrating/', views.starrating, name='starrating'),

]