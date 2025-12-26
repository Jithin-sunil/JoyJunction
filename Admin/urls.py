from django.urls import path
from Admin import views
app_name = 'Admin'
urlpatterns = [
    path('',views.Homepage,name='Homepage'),

    path('AdminRegistration/',views.AdminRegistration,name='AdminRegistration'),
    path('deladmin/<int:did>/',views.deladmin,name='deladmin'),
    path('editadmin/<int:eid>/',views.editadmin,name='editadmin'),

    path('District/',views.District,name='District'),
    path('deldistrict/<int:did>/',views.deldistrict,name='deldistrict'),
    path('editdistrict/<int:eid>/',views.editdistrict,name='editdistrict'),

    path('Place/',views.Place,name='Place'),
    path('delplace/<int:did>/',views.delplace,name='delplace'),
    path('editplace/<int:eid>/',views.editplace,name='editplace'),

    path('Category/',views.Category,name='Category'),
    path('delcategory/<int:did>/',views.delcategory,name='delcategory'),
    path('editcategory/<int:eid>/',views.editcategory,name='editcategory'),

    path('SubCategory/',views.SubCategory,name='SubCategory'),
    path('delsubcategory/<int:did>/',views.delsubcategory,name='delsubcategory'),
    path('editsubcategory/<int:eid>/',views.editsubcategory,name='editsubcategory'),

    path('SellerVerification/',views.SellerVerification,name='SellerVerification'),
    path('verifyseller/<int:vid>/',views.verifyseller,name='verifyseller'),
    path('rejectseller/<int:rid>/',views.rejectseller,name='rejectseller'),

    path('UserList/', views.UserList, name='UserList'),

    path('ViewComplaint/', views.ViewComplaint, name='ViewComplaint'),
    path('ReplyComplaint/<int:cid>/', views.ReplyComplaint, name='ReplyComplaint'),
]