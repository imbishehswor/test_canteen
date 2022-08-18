from tkinter import Menu
from django.urls import path
from . import views
urlpatterns = [

    
    path('productlist',views.login),
    path('registerPage',views.registerPage),
    path('register',views.register),
    path('signupVarification',views.signupVarification),
    path('otp',views.otp),
    path('login',views.login),
    path('users',views.users),
    path('changePassword/<int:id>', views.changePassword),
    path('changePasswordAdmin/<int:id>', views.changePasswordAdmin),
    path('history/<int:id>',views.orderHistory),
    path('Admin_see_history/<int:id>',views.Admin_see_history),
    path('profile/<int:id>',views.profile),
    path('logout/final',views.logout, name="logout"),
    path('accounts-menu',views.accountsMenu, name="accounts"),
    path('accounts-orderList',views.orderList, name="orderlist"), 
    path('addUser',views.addUser, name="adduser"), 
    path('finalAdduser',views.finalAdduser, name="finalAdduser"), 
    path('editUSer/<int:id>',views.editUSer, name="editUSer"), 
    path('deleteUser/<int:id>',views.deleteUser, name="deleteUser"), 
    path('finalEdituser/<int:id>',views.finalEdituser, name="finalEdituser"), 



    path('forgotPassword/',views.forgotPassword,name="forgotPassword"),
    path('forgetPasswordOTP',views.forgetPasswordOTP,name="forgetPasswordOTP"),
    path('fogetOTPvaryfyChangePassword',views.fogetOTPvaryfyChangePassword,name="fogetOTPvaryfyChangePassword"),
    path('final_Forget_Change_Password',views.final_Forget_Change_Password,name="final-Forget-Change-Password"),

     


   




    # path('test',views.test),
   
    # path('llogin',views.llogin),
]
