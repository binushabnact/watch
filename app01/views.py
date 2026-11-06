

from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from .models import register, addprt, Cart, Order


def index(request):
    return HttpResponse("Hello World")



# Create your views here.
def Home(request):
    template = loader.get_template("home.html")
    return HttpResponse(template.render({},request))

def Register(request):
    if 'usersession' in request.session:
        return HttpResponseRedirect('/')
    if request.method=='POST':
        reg_firstname=request.POST['register_fname']
        reg_lastname = request.POST['register_lname']
        reg_phone = request.POST['register_phone']
        reg_email = request.POST['register_email']
        reg_user = request.POST['register_user']
        reg_password = request.POST['register_password']

        reg=register(
          contact_firstname=reg_firstname,
          contact_lastname=reg_lastname,
          contact_Phone=reg_phone,
          contact_Email=reg_email,
          contact_Uer=reg_user,
          contact_Password=reg_password
        )
        reg.save()

        return HttpResponseRedirect('/login')
    return render(request,'Register.html')

def login(request):
   if'usersession'in request.session:
      return HttpResponseRedirect('/')
   if request.method == "POST":
     log_id=request.POST['log_id']
     log_psd = request.POST['log_psd']

     login=register.objects.filter(
        contact_Uer=log_id,
         contact_Password=log_psd,
     )
     if login:
      request.session['usersession']=log_id
      return HttpResponseRedirect('/')
   template = loader.get_template("login.html")
   return HttpResponse(template.render({}, request))
def account(request):
   if 'usersession' not in request.session:
      return HttpResponseRedirect('/login')
   template=loader.get_template("account.html")
   return HttpResponse(template.render({},request))
def logout_view(request):
    logout(request)
    return redirect('login')

def addproduct(request):
    if 'usersession' not in request.session:
        return HttpResponseRedirect('/login')
    if request.method=='POST':
        pro_name=request.POST.get('pro_name')
        pro_price = request.POST.get('pro_price')
        pro_image = request.FILES.get('pro_image')

        product=addprt(
            pro_name=pro_name,
            pro_price=pro_price,
            pro_image=pro_image
        )
        product.save()
        return HttpResponseRedirect('/addproduct')

    template=loader.get_template("addproduct.html")
    return HttpResponse(template.render({},request))

def view_product(request):

 products=addprt.objects.all().values()


 context={
     'products':products
 }
 template=loader.get_template("shop.html")
 return HttpResponse(template.render(context,request))

def addtocart(request,id):

    if 'usersession' not in request.session:
        return HttpResponseRedirect('/login')

    exist = Cart.objects.filter(cart_proid=id,
    cart_user=request.session["usersession"])

    if exist:
        exstcart = Cart.objects.filter(cart_proid=id, cart_user=request.session["usersession"])[0]

        exstcart.cart_qty+=1
        exstcart.cart_amount=exstcart.cart_qty * exstcart.cart_price
        exstcart.save()
    else:

        pro = addprt.objects.filter(id=id)[0]

        cart = Cart(cart_user=request.session["usersession"],
                    cart_proid=pro.id,
                    cart_name=pro.pro_name,
                    cart_price=pro.pro_price,
                    cart_image=pro.pro_image,
                    cart_qty=1,
                    cart_amount=pro.pro_price)
        cart.save()

    return HttpResponseRedirect("/cart")

def cart(request):

    if 'usersession' not in request.session:
        return HttpResponseRedirect('/login')

    if 'del' in request.GET:
        id = request.GET['del']
        delcart = Cart.objects.filter(id=id)[0]
        delcart.delete()

    if 'q' in request.GET:
        q = request.GET['q']
        cp =request.GET['cp']
        cart3=Cart.objects.filter(id=cp)[0]

        if q=='inc':
            cart3.cart_qty+=1
        elif q=='dec':
            if(cart3.cart_qty>1):
                cart3.cart_qty-=1

        cart3.cart_amount = cart3.cart_qty * cart3.cart_price
        cart3.save()


    user = request.session["usersession"]
    cart=Cart.objects.filter(cart_user=user).values()
    cart2=Cart.objects.filter(cart_user=user)

    tot = 0
    for x in cart2:
        tot+=x.cart_amount

    shp = tot * 10/100
    gst = tot * 18/100

    gtot = tot+shp+gst

    request.session["tot"] = tot
    request.session["gst"] = gst
    request.session["shp"] = shp
    request.session["gtot"] = gtot

    context={

        'cart':cart,
        'tot':tot,
        'gst':gst,
        'gtot':gtot
    }

    template=loader.get_template("cart.html")
    return HttpResponse(template.render(context,request))

def checkout(request):

    if 'usersession' not in request.session:
        return HttpResponseRedirect('/login')

    co = 0
    adrs = ptype = ""

    if 'dlv_adrs' in request.POST:
        adrs = request.POST["dlv_adrs"]
        ptype = request.POST["pay_type"]
        co = 1

    user = request.session["usersession"]

    old_odr=Order.objects.filter(order_user=user,order_status=0)
    old_odr.delete()


    cart=Cart.objects.filter(cart_user=user)
    for x in cart:
        odr = Order(order_user=x.cart_user,
                    order_name=x.cart_name,
                    order_price=x.cart_price,
                    order_image=x.cart_image,
                    order_qty=x.cart_qty,
                    order_amount=x.cart_amount,
                    order_address=adrs,
                    order_paytype=ptype,
                    order_status=0
                )
        odr.save()
    order=Order.objects.filter(order_user=user,order_status=0).values()

    tot = request.session["tot"]
    gst = request.session["gst"]
    shp = request.session["shp"]
    gtot = request.session["gtot"]


    context={

        'order':order,
        'tot':tot,
        'shp':shp,
        'gst':gst,
        'gtot':gtot,
        'co':co
    }

    template = loader.get_template("checkout.html")
    return HttpResponse(template.render(context,request))

def confirmorder(request):

    if 'usersession' not in request.session:
        return HttpResponseRedirect('/login')

    user = request.session["usersession"]

    order=Order.objects.filter(order_user=user,order_status=0)

    for x in order:
        x.order_status=1
        x.save()

    template = loader.get_template("confirmorder.html")
    return HttpResponse(template.render({},request))

def myorders(request):
    user = request.session["usersession"]

    order=Order.objects.filter(order_user=user,order_status=1)

    context = {
        'order':order
    }
    template = loader.get_template("myorders.html")
    return HttpResponse(template.render(context,request))
