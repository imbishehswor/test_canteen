# from email import message
from ast import Pass
from contextlib import redirect_stderr
from urllib.parse import uses_relative
from django.views.decorators.csrf import csrf_exempt
from email.policy import HTTP
from itertools import product
import random
from xmlrpc.client import TRANSPORT_ERROR
import django
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.core import mail
from requests import request
from .models import Users
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from product.models import Product
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash 


# Create your views here.

# def accounts(request):

@csrf_exempt
def addUser(request):
   
   

    return render(request,"admin/adduser.html")

def editUSer(request,id):
    user = Users.objects.get(id = id)

    return render(request,'admin/editUser.html',{'user':user})

def deleteUser(request,id):
    user = Users.objects.filter(id = id)
    user.delete()
    auth_user = User.objects.filter(id = id)
    auth_user.delete()
    
    return redirect("http://127.0.0.1:8000/accounts/users")



def finalEdituser(request,id):
    
    if request.method == "POST":
        user_fullname = request.POST.get('user_fullname')
        user_phone = request.POST.get('user_phone')

        user = Users.objects.get(id= id)
        user.user_fullname = user_fullname
        user.user_phone = user_phone
        user.save()
        messages.success(request,"successfully edited!!")

        return redirect("http://127.0.0.1:8000/accounts/users")



def finalAdduser(request):
    if request.method == "POST":
        user_fullname = request.POST.get('user_fullname')
        user_email = request.POST.get('user_email')
        user_phone = request.POST.get('user_phone')
        user_password = request.POST.get('user_password')

        x = user_fullname.split()

        user = User.objects.create_user(username = user_email,password=user_password,email=user_email,first_name=x[0],last_name = x[1])
        user.save()
        db = Users(user_fullname= user_fullname, user_phone=user_phone,user_email=user_email,user_password= user_password,user_role=False)
        db.save()
        auth_login(request,user)
        messages.success(request,"User created success fully!!!!!")
    
    return redirect("http://127.0.0.1:8000/accounts/addUser")





def orderList(request):
    if (request.user.is_authenticated and request.session.get('user_role')==True):

        orderList = Product.objects.raw("select oi.id,oi.date,u.user_fullname as Order_By,p.product_photo, p.product_name,p.product_price,od.quantity, p.product_price*od.quantity as total from order_item oi inner join users u on u.id = oi.user_id join order_details od  on od.order_id = oi.id join product p on p.id = od.product_id order by oi.date desc;")
                    
        # messages.info(request, "Logged in successfully")
        return render(request,'product/profileOrderlist.html',{"orderList":orderList})
    else:
        return redirect("http://127.0.0.1:8000/accounts/login")


def accountsMenu(request):

    prod = Product.objects.filter(product_active = True)

    return render(request,'nuser/menu.html',{'prod':prod})

def logout(request):
    
    auth_logout(request)
    request.session.clear()
    return redirect('/')
# def logout(request):
#     request.session.clear()
    
#     return redirect("http://127.0.0.1:8000/accounts/login")



def profile(request,id):

    return render(request,'nuser/profile.html')
    
def showLoginpage(request):

    return render(request,'user/login.html')

@csrf_exempt
def login(request):
    username = ''
    password = ''
    if request.method == "POST":
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        print (user)

        if user is not None:
            request.session.clear()
            auth_login(request, user)
            
            userInfo = Users.objects.get(user_email=user)

            request.session['user_id']=userInfo.id
            request.session['user_fullname'] = userInfo.user_fullname
            request.session['user_email'] = userInfo.user_email
            request.session['user_phone']=userInfo.user_phone

            request.session['user_role'] = userInfo.user_role
            

            request.session['user_fullname']=userInfo.user_fullname
            # messages.info(request, "Logged in successfully")
            # return redirect('/')
            if userInfo.user_role == True:
                # orderList = Product.objects.raw("select oi.id,u.user_fullname as Order_By,p.product_photo, p.product_name,p.product_price,od.quantity, p.product_price*od.quantity as total from order_item oi inner join users u on u.id = oi.user_id join order_details od  on od.order_id = oi.id join product p on p.id = od.product_id")
                # status = "SuperUser"
                # messages.info(request, "Logged in successfully")
                #return render(request,'product/profileOrderlist.html',{"orderList":orderList,"user":userInfo})
                return redirect("http://127.0.0.1:8000/accounts/accounts-orderList")
                
            else:
                # prod = Product.objects.all()
                status = "normal user"
                prod = Product.objects.all()
                # return render(request,'nuser/menu.html',{'prod':prod,"user":userInfo})
                return redirect("http://127.0.0.1:8000/accounts/accounts-menu")
                

            # return render(request,'product/profileOrderlist.html')
        else:
            messages.warning(request,"Invalid username and pasword!!")
            return render(request,"user/login.html")
        
    return render(request,"user/login.html")


def registerPage(request):
   
    n = random.randint(1111,9999)
    request.session['otpnum']=n
      
    return render(request,'user/register.html')

def register(request):
   
    print(request.session.get('otpnum'))
    

      
    return render(request,'user/register.html')



def signupVarification(request):
    global email_address,name,phone,password
    if request.method == "POST":
        email_address = request.POST.get('user_email')
        request.session['register_email_address']  = email_address 
        name = request.POST.get('user_fullname')
        request.session['register_name'] = name
        request.session['register_phone'] = request.POST.get('user_phone')
        request.session['register_password'] = request.POST.get('user_password1')


    def sentMail(email): 
       
        em = email
        connection = mail.get_connection()

        connection.open()
        n =request.session.get('otpnum')

        
        email1 = mail.EmailMessage(
            'Email verification ',
            " Dear User, \n          This is system generated Email please do not reply to this Email ID.  \n\n OTP Code:"+str(n)+"\n\n\n\n\n BEST REGARDS, \n Bisheshwor Khadka",
            'bisheshwor.khadka@apexcollege.edu.np',
            [em],
            connection=connection,
        )

        email1.send()

        connection.close()

    if (User.objects.filter(username = email_address).exists() or User.objects.filter(email = email_address).exists()):
        messages.warning(request, "Username is already exists! ")
        return redirect("http://127.0.0.1:8000/accounts/registerPage")
    else: 

        sentMail(email_address)
        return render(request,'user/verify.html',{'email':email_address,'name':name})



def otp(request):
    # cn = "something" 

    if request.method == "POST":
        otpCode = request.POST.get('otp')
        n = request.session.get('otpnum')
        
        sn = str(n)
        print(n)
        print(otpCode)
        # request.session['register_email_address'] = request.POST.get('user_email')
        # request.session['register_name'] = request.POST.get('user_fullname')
        # request.session['register_phone'] = request.POST.get('user_phone')
        # request.session['register_password'] = request.POST.get('user_password1')
        name = request.session.get('register_name')
        email_address = request.session.get('register_email_address')
        phone = request.session.get('register_phone')
        password = request.session.get('register_password')

         





        if otpCode == sn: 
            user = User.objects.create_user(username = email_address,password=password,email=email_address,first_name=name)
            user.save()
            db = Users(user_fullname= name, user_phone=phone,user_email=email_address,user_password= password,user_role=False)
            db.save()
            auth_login(request,user)
            # messages.success(request,"User successfully Created")
            return redirect('http://127.0.0.1:8000/accounts/login')
        else:
            print("different")


    return render(request,'user/otp.html')



def users(request):
    
    user = Users.objects.all()
    return render(request,"user/user.html",{'user':user})


#@login_required #(redirect_field_name='account')
# @login_required
def orderHistory(request,id):
    if(request.user.is_authenticated):
        sql = "select 1 id, u.user_fullname, oi.date,p.product_photo, p.product_name,p.product_price,od.quantity,od.quantity,od.quantity*p.product_price as total_cost from order_item oi inner join users u on u.id = oi.user_id join order_details od on od.order_id = oi.id join product p on p.id = od.product_id where u.id ="+str(id)+" ;"
        
        totalBill = 0 
        oh = Product.objects.raw(sql)
        username = ''
        for i in oh:
            totalBill = totalBill+i.quantity * i.product_price
            username =  i.user_fullname
        
        print("your Total bill is: ",totalBill)
        return render(request,'user/history.html',{'oh':oh,'totalBill':totalBill,'username':username})
    else:
        return redirect('http://127.0.0.1:8000/accounts/login')

def Admin_see_history(request,id):
    if (request.user.is_authenticated and request.session.get('user_role')==True ):
        sql = "select 1 id, u.user_fullname, oi.date,p.product_photo, p.product_name,p.product_price,od.quantity,od.quantity,od.quantity*p.product_price as total_cost from order_item oi inner join users u on u.id = oi.user_id join order_details od on od.order_id = oi.id join product p on p.id = od.product_id where u.id ="+str(id)+" ;"
        
        totalBill = 0 
        oh = Product.objects.raw(sql)
        username = ''
        for i in oh:
            totalBill = totalBill+i.quantity * i.product_price
            username =  i.user_fullname
        
        # print("your Total bill is: ",totalBill)
        return render(request,'admin/admin_see_useHistory.html',{'oh':oh,'totalBill':totalBill,'username':username})
        



    else:
        return redirect('http://127.0.0.1:8000/accounts/login')


def changePassword(request,id):
    if (request.user.is_authenticated):
        if request.method == "POST":
            form = PasswordChangeForm(request.user, request.POST)
            
            if form.is_valid():
                v = form.save()
                update_session_auth_hash(request, v)
                return HttpResponse("Success")
        else:

            form = PasswordChangeForm(request.user)
            print("sorry")
        params = {
            'form':form,
        }
        # user = Users.objects.get(id =id)
        # if request.method == 'POST':
        #     oldpass = request.POST.get('oldpassword')
        #     pass1 = request.POST.get('pass1')
        #     pass2 = request.POST.get('pass2')

        #     if user.user_password == oldpass:
            
        #         user.user_password = pass1
        #         user.save()

        #         messages.success(request,"password changenged succesfully")
             
        return render(request,'user/changepassword.html',params)
    else:
        return redirect("http://127.0.0.1:8000/accounts/login")


def changePasswordAdmin(request,id):
    if (request.user.is_authenticated and request.session.get('user_role')==True):
        user = Users.objects.get(id =id)
        if request.method == 'POST':
            oldpass = request.POST.get('oldpassword')
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')

            if user.user_password == oldpass:
            
                user.user_password = pass1
                user.save()

                messages.success(request,"password changenged succesfully")
            
        return render(request,'admin/admin_changepassword.html')
    else:
        return redirect("http://127.0.0.1:8000/accounts/login")
    




def forgotPassword(request):
    n = random.randint(1111,9999)
    request.session['forgotOTPcode'] = n

    return render(request,'user/forgetPassword.html')
   

def forgetPasswordOTP(request):
    if request.method == "POST":
        user_email = request.POST.get('username')
        request.session['forgetEmail']=user_email
        print("user email is", user_email)

    if (User.objects.filter(username = user_email).exists() or User.objects.filter(email = user_email).exists()):
        n = request.session.get('forgotOTPcode')

        def sentMail(email):
            print("function called")
            em = email
            connection = mail.get_connection()
            

            connection.open()

            # global cn
            # cn = str(n)
            email1 = mail.EmailMessage(
                'Email verification ',
                " Dear User, \n          Your you are forget your password so password reset code is .  \n\n OTP Code:"+str(n)+"\n\n\n\n\n BEST REGARDS, \n Bisheshwor Khadka",
                'bisheshwor.khadka@apexcollege.edu.np',
                [em],
                connection=connection,
            )

            email1.send()
            connection.close()
       
        sentMail(user_email)
        
    else:
        
            messages.warning(request, "Your email is not register yet! ")
            return redirect("http://127.0.0.1:8000/accounts/login")
    
    return render(request,"user/forgotPassOTP.html")



def fogetOTPvaryfyChangePassword(request):
    n = request.session.get('forgotOTPcode')
    if request.method == "POST":
        otp = request.POST.get('otp')

        if otp == str(n):
            return render(request,'user/forgetChangePassword.html')
        else:
            return HttpResponse("otp doesnot matched!")

    return HttpResponse("success")

def final_Forget_Change_Password(request):
    forgetEmail = request.session.get('forgetEmail')

    if request.method == "POST":
        newPassword = request.POST.get('pass1')
    
    obj = User.objects.get(username = forgetEmail)
    # obj.password = newPassword
    obj.set_password(newPassword)
    obj.save()

    messages.success(request,"password changenged succesfully")
    
    return redirect("http://127.0.0.1:8000/accounts/login")


   


   