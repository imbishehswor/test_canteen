from asyncio.windows_events import NULL
from contextlib import redirect_stderr
import imp
from django.contrib import messages
from types import NoneType
from django.http import HttpResponse
from django.shortcuts import render,redirect
from product.models import Product
from accounts.models import Users
from django.db import transaction
from orderItems.models import Order_items,Order_details
from orderItems.models import Qrcode
import qrcode
import qrcode.image.svg
from io import BytesIO



# Create your views here.
def cancelOrder(request):
    if request.user.is_authenticated:
       
        return redirect("http://127.0.0.1:8000/products/menu")
    else:
        return redirect('http://127.0.0.1:8000/accounts/login')


def add_to_cart(request):
    
    if request.method == "POST":
            product_id = request.POST.get('product_id')
            quantity = request.POST.get('quantity')
    

    cart = request.session.get('cart')
    if cart:

        cart[product_id] = quantity

    else:
        cart = {}
        cart[product_id] =quantity
    
    request.session['cart'] = cart

    print("the cart is:",request.session.get('cart'))
   
    return redirect('http://127.0.0.1:8000/products/menu')




def coformOrder(request):
    cartDictionary = request.session.get('cart')

    if (bool(cartDictionary) == False):

        messages.success(request,"you have not select any food yet!!")
        return redirect("http://127.0.0.1:8000/products/menu")
        
    else:

        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        # print("products: ",products)
        # for product in products:
        #     print("name:",product.product_name )
        # ivs = list(request.session.get('cart').values())
        # print(ivs)
        
        return render(request,'order/cart.html',{'products':products})

def deleteItemCart(request,id):
    productDictionary = request.session.get('cart')
    del productDictionary[str(id)]
    
    request.session['cart']=productDictionary

    return redirect("http://127.0.0.1:8000/order/coformOrder")

def editCart(request,id):
    quantity = 0
    productDictionary = request.session.get('cart')
    prod = Product.objects.get(id =id)
    for key ,value in productDictionary.items():
        # print(type(id))
        # print(type(key))
        
        if key == str(id):
            quantity = value
            return render(request,"product/editCart.html",{'quantity':quantity,'prod':prod})
        
def finalCartEdit(request,id):
    productDictionary = request.session.get('cart')

    if request.method == "POST":
        quantity = request.POST.get('quantity')
        upload = {str(id):quantity}
       
        productDictionary.update(upload)
        request.session['cart'] = productDictionary
        return redirect("http://127.0.0.1:8000/order/coformOrder")

    return HttpResponse("edit")


        



def multipleOrder(request):
   

    productDictionary = request.session.get('cart')
    print("YOUT ID IS ::::::",request.session.get('user_id'))
    


        

    sid = NULL
    try:
        with transaction.atomic():
            u_id = request.session.get('user_id')
            print("user Id is ::::", u_id)
            user_id = Users.objects.get(id = u_id)
            Order_items.objects.create(
                user = user_id
            )
            # ot = Order_items(user= uid)
            # ot.save()
            print("successfully inserted")
            global last_id
            last_id = Order_items.objects.latest('id').id
           
            # print(last_obj)
            order_id = Order_items.objects.get(id = last_id)
            
            for key,value in productDictionary.items():
                productID = Product.objects.get(id=key)
                qty = value
                
                product_info = Product.objects.filter(id = key)
                for i in product_info:
                    pprice = i.product_price
                    

            
                Order_details.objects.create(
                    order = order_id,
                    product = productID,
                    quantity = qty
                )
    except Exception as e:
        print(e)
        transaction.savepoint_rollback(sid)
        print("error in transaction")
    
    
    
    u_id = request.session.get('user_id')
            
  
    sql = "select oi.id,u.id as user_id,u.user_fullname, p.product_name,p.product_price,od.quantity from order_item oi inner join users u on u.id = oi.user_id join order_details od on od.order_id = oi.id join product p on p.id = od.product_id where oi.id ="+str(last_id)+" ;"
    # qr = Qrcode.objects.get(user_id = u_id)
    qr = Qrcode.objects.filter(user_id = u_id)
    # qr = Qrcode.objects.raw("SELECT * FROM qrcode where user_id = "+ str(u_id)+";")

    sod = NULL
    try:
        # with transaction.atomic():
        #     for i in qr:
        #         if i.user_id == u_id:
            # qr.delete()
            # Qrcode.objects.raw("delete from qrcode where user_id ="+str(u_id)+";")
            for i in qr:
                i.delete()
                
            print("data deleted")

            for i in Product.objects.raw(sql):
                obj = Qrcode.objects.create( order_id = i.id,user_fullname = i.user_fullname,product_name = i.product_name,product_price = i.product_price,quantity = i.quantity,user_id = i.user_id)


                obj.save()
            print("qr table inserted")


    except Exception as e:
        print(e)
        transaction.savepoint_rollback(sod)
        print("error in transaction")

    red = "http://127.0.0.1:8000/order/finalQRcode/"+str(u_id)

    return redirect(red)


def finalQRcode(request,id):
    total_message = ''
    sum = 0
    sql = "select  q.id, oi.date, q.user_fullname, q.product_name,q.product_price,q.quantity,q.user_id  from qrcode q inner join order_item oi on oi.id = q.order_id where q.user_id = "+str(id)+";"
    # sql = "select oi.id,u.user_fullname, p.product_name,p.product_price,od.quantity from order_item oi inner join users u on u.id = oi.user_id join order_details od on od.order_id = oi.id join product p on p.id = od.product_id where oi.id ="+str(last_id)+" ;"
    for i in Product.objects.raw(sql):
        message = "(((Order Date::::::: "+str(i.date)+" )))"+"\n\n\n"+"order by: "+str(i.user_fullname)+"\n"+"product No: "+str(i.product_name)+"\n product price: "+str(i.product_price)+"\n product Quantity: "+str(i.quantity)+ "\n total cost of "+str(i.product_name)+"is: "+str(i.product_price*i.quantity)+ "\n\n\n\n"
        # message = "\tname \t \t  "+ "product_name\t\t product_price \t\t quantity\t\t totalcost\n"+str(i.user_fullname) +" \t\t"+str(i.product_name)+"\t\t"+str(i.product_price)+"\t\t \t\t"+str(i.quantity )+ "\t\t"+ str(i.product_price*i.quantity)+'\n'
        total_message = str(total_message)+message
        print(message)
        sum = sum+i.product_price*i.quantity
    total_message= total_message+"\n\n ::Total Amount::"+str(sum)
    context = {}
    
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(total_message, image_factory=factory, box_size=20)
    stream = BytesIO()
    img.save(stream)
    context["svg"] = stream.getvalue().decode()

    return render(request, "order/qr.html", context=context)







    