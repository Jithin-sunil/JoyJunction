from django.urls import path
from User import views
app_name = 'User'
urlpatterns = [
    path('Homepage/', views.Homepage, name='Homepage'),
    path('Myprofile/', views.Myprofile, name='Myprofile'),
    path('EditProfile/', views.EditProfile, name='EditProfile'),
    path('ChangePassword/', views.ChangePassword, name='ChangePassword'),
]