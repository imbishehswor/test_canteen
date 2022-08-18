from django.shortcuts import redirect, render,HttpResponse
from .forms import productForm
from .models import Product
from django.contrib import messages

def uploadProduct(request):
    if (request.user.is_authenticated and request.session.get('user_role')==True):

        context = {}    
        if request.method == "POST": 
            form = productForm(request.POST, request.FILES) 
            if form.is_valid(): 
                pname = form.cleaned_data.get("product_name") 
                pphoto = form.cleaned_data.get("product_photo") 
                pdesc = form.cleaned_data.get("product_desc") 
                pprice = form.cleaned_data.get("product_price") 
                pactive = form.cleaned_data.get("product_active")
                obj = Product.objects.create(product_name = pname,product_photo = pphoto,product_desc = pdesc, product_price=pprice,product_active = pactive) 
                obj.save() 
                messages.success(request,"product added successfully")
                print(obj)
                # return redirect('success') 
                return redirect("http://127.0.0.1:8000/products/addProducts")
                # message.success(request,"product added successfully")
                # print("Product added successfully")
        else: 
            form = productForm()
            context['form'] = form
            return render( request, "product/addproduct.html", context) 
    else:
         return redirect('http://127.0.0.1:8000/accounts/login')


def showProduct(request):
    if (request.user.is_authenticated and request.session.get('user_role')==True):
        # request.session.get('cart').clear()
        print("you are : ",request.session.get('user_fullname'))

        prod = Product.objects.all()

        return render(request,'product/product.html',{'prod':prod})
    else:
        return redirect('http://127.0.0.1:8000/accounts/login')


def deleteProduct(request,id):
    if (request.user.is_authenticated and request.session.get('user_role')==True):

        prod = Product.objects.filter(id = id)
        prod.delete()
    

        return redirect("http://127.0.0.1:8000/products/viewProduct")
    else:
        return redirect('http://127.0.0.1:8000/accounts/login')
    

def editProduct(request,id):
    if (request.user.is_authenticated and request.session.get('user_role')==True):
        prod = Product.objects.filter(id=id)
        for i in prod:
            print(i.product_desc)

        return render (request,"product/editProduct.html",{'prod':prod})
    else:
        return redirect('http://127.0.0.1:8000/accounts/login')
    
def updateProduct(request,id):
    if (request.user.is_authenticated and request.session.get('user_role')==True):

        if request.method =="POST":
            pname = request.POST.get('product_name')
            pprice = request.POST.get('product_price')
            pdescription = request.POST.get('product_desc')
            
            prod = Product.objects.get(id=id)
            product_name = request.POST.get('product_name')
            product_price = request.POST.get('product_price')
            product_desc = request.POST.get('product_desc')
        
        # sql = "update product set product_name = '"+str(product_name)+"',product_price = "+str(product_price)+",product_desc = '"+str(product_desc)+"' where id = "+str(id)+";"
        # a = Product.objects.raw(sql)
        # print(a)
        prod = Product.objects.get(id=id)
        prod.product_name = product_name
        prod.product_price = product_price
        prod.product_desc = product_desc
        prod.save()
        messages.success(request,"Product edited successfully!")

        return redirect("http://127.0.0.1:8000/products/viewProduct")
    else:

        return redirect('http://127.0.0.1:8000/accounts/login')


def menu(request):
    if(request.user.is_authenticated):

        prod = Product.objects.all()

        return render(request,"nuser/menu.html",{'prod':prod})
    return redirect('http://127.0.0.1:8000/accounts/login')


def dailyUpdate(request):
    if (request.user.is_authenticated and request.session.get('user_role')==True):

        prod = Product.objects.all()

        if request.method == "POST":
            check = request.POST.getlist('checks[]')

            # for i in check:
            #     for p in prod:
            #         if p.id == i:
            #             print("productName::::::::::::::::::::::",p.product_name)
            #  
            # for p in prod:
            #     for i in check:
            #         if p.id == i:
            #             print("productName::::::::::::::::::::::",p.product_name)
            #         else: print("sorry::::::::::::::::::::::::::::::::::::::")

            # for p in prod:
            #     for i in check:
            #         if str(p.id) == i:
            #             print ("mutual id::::::::::::",p.product_name)
            #             # p.product_active = True
            #             # p.save()
            #             check.remove(i)
            #             p.remove()
            #             # p.remove(p.id)
            #         # else:
            #     print("non mutyual id:::::::",p.product_name)
            #     # p.product_active = False




            

            for p in prod:
                print()
                # print("type of::",type(p.id))
                if str(p.id) in check:
                    
                    p.product_active = True
                    p.save()

                else:
                    p.product_active = False
                    p.save()
                
                # p = Product.objects.get(id = i)
                # if str(p.id) == i:
                #     print("heloo:::::::::",p.id)
                #     p.delete()
                # else:
                #     print("Hello ::::::::::::",p.id)
            



            # for i in check:
                # p = Product.objects.get(id = i)
                # # print(p.product_name)
                # p.product_active = True
                # p.save()



                # for p in prod:
                #     if str(p.id) == i:
                #         p.product_active = True
                #         p.save()
                #         print("yes")
                #     else:
                #         p.product_active = False
                #         p.save()
                #         print("sorry")


                # print("product",type(p.id))
                # print("check",type(i))
            # for p in prod:
            #     for i in check:
            #         if i == p.id:
            #             print("hellooooo")
            #         else:
            #             print("HII")

        
        total = len(prod)
        return render(request,"product/Dupdate.html",{"prod":prod,'total':total})
    else:
        return redirect('http://127.0.0.1:8000/accounts/login')